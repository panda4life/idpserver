# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 10:59:45 2014

@author: James Ahad
"""

from django import forms

from django.contrib.auth.models import User
from idp.models import UserProfile, Sequence, Sequence_seqdata, Sequence_jobs
class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()

import idp.computation as comp
class SingleSequenceForm(forms.Form):
    seq = forms.CharField(max_length = None, help_text = "Please enter an amino acid sequence")
    tag = forms.CharField(max_length=None, help_text = "Give your sequence a label")
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SingleSequenceForm, self).__init__(*args, **kwargs)
    def save(self):
        seqstring = self.cleaned_data['seq']
        computeSeq = comp.Sequence(seqstring)
        from django.utils import timezone
        newSequence = Sequence(seq = seqstring,
                               tag = self.cleaned_data['tag'],
                               user = self.user,
                               submissionDate = timezone.now(),
                               seqProc = False,
                               jobProc = False,)
        newSequence.save()
        newSeqData = Sequence_seqdata(seq = newSequence,
                                        fplus = round(computeSeq.Fplus(),5),
                                        fminus = round(computeSeq.Fminus(),5),
                                        FCR = round(computeSeq.FCR(),5),
                                        NCPR = round(computeSeq.NCPR(),5),
                                        meanH = round(computeSeq.meanHydropathy(),5),
                                        sigma = round(computeSeq.sigma(),5),
                                        delta = round(computeSeq.delta(),5),
                                        dmax = round(computeSeq.deltaMax(),5),
                                        kappa = round(computeSeq.kappa(),5))
        newSeqData.save()
        newSequence.seqProc = True
        newSequence.save()
        return self.user

class MultiSequenceForm(forms.Form):
    seqlist = forms.CharField(widget=forms.Textarea(attrs={'cols': 500, 'rows':10}), help_text = "Please enter amino acid sequences separated by carraige returns")
    tag = forms.CharField(max_length=None, help_text = "Please enter your sequence category")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(MultiSequenceForm, self).__init__(*args, **kwargs)
    def save(self):
        seqlist = self.cleaned_data['seqlist']
        for seqstring in seqlist.split('\n'):
            if(Sequence.objects.filter(seq = seqstring, user = self.user).exists()):
                continue
            computeSeq = comp.Sequence(seqstring)
            from django.utils import timezone
            newSequence = Sequence(seq = computeSeq.seq,
                                   tag = self.cleaned_data['tag'],
                                   user = self.user,
                                   submissionDate = timezone.now(),
                                   seqProc = False,)
            newSequence.save()
            newSeqData = Sequence_seqdata(seq = newSequence,
                                            N = computeSeq.len,
                                            fplus = computeSeq.Fplus(),
                                            fminus = computeSeq.Fminus(),
                                            FCR = computeSeq.FCR(),
                                            NCPR = computeSeq.NCPR(),
                                            meanH = computeSeq.meanHydropathy(),
                                            sigma = computeSeq.sigma(),
                                            delta = computeSeq.delta(),
                                            dmax = computeSeq.deltaMax(),
                                            kappa = computeSeq.kappa())
            newSeqData.save()
            newSequence.seqProc = True
            newSequence.save()
'''
class tagForm(forms.Form):
    tag = forms.CharField(widget=forms.SelectMultiple, help_text = "What Sequences do you want to work with?")

    def __init__(self, user, nextForm, *args, **kwargs):
        self.user = user
        self.nextForm = nextForm
        super(MultiSequenceForm, self).__init__(*args, **kwargs)

    def save(self):
'''
class wl_JobForm(forms.Form):
    seq = forms.ModelChoiceField(Sequence.objects.none(), help_text = 'Select sequence to solve for Kappa DoS')
    #seq = forms.ModelMultipleChoiceField(Sequence.objects.all())
    genPermutants = forms.NullBooleanField(help_text='Would you like to generate Kappa sequence permutants?')

    def __init__(self,user, *args, **kwargs):
        super(wl_JobForm,self).__init__(*args, **kwargs)
        self.user = user
        #q = Sequence.objects.all()
        q = Sequence.objects.filter(user = self.user)
        self.fields['seq'].queryset = q.extra(order_by = ['tag'])

    def launchJob(self):
        seqchoice = self.cleaned_data['seq']
        newJob = Sequence_jobs(seq = seqchoice, user = self.user)
        from django.conf import settings
        if(self.cleaned_data['genPermutants']):
            newJob.jobType = 'wlp'
            newJob.jobTypeVerbose = 'Wang Landau \w Permutant Generation'
            newJob.jobParameters = ''
        else:
            newJob.jobType = 'wl'
            newJob.jobTypeVerbose = 'Wang Landau'
            newJob.jobParameters = ''
        newJob.status = 'launched'
        import os
        from extraFuncs import create_path
        newJob.outdir = os.path.join(settings.DAEMON_OUT_PATH,os.path.normpath("%d/%d/%s/" % (newJob.user.pk, newJob.seq.pk, newJob.jobType)))
        create_path(newJob.outdir)
        newJob.progressFile = os.path.join(newJob.outdir, 'progress.txt')
        inputFilePath = os.path.normpath("%s/%d_%d_%s" % (settings.DAEMON_IN_PATH, newJob.user.pk, newJob.seq.pk, newJob.jobType))
        create_path(os.path.dirname(inputFilePath))
        if(Sequence_jobs.objects.filter(seq = newJob.seq, jobType = newJob.jobType).exists()):
            newJob.status = 'ar'
            return newJob
        newJob.save()
        with open(inputFilePath, 'w') as f:
            f.write('User %s\n' % newJob.user.username)
            f.write('First %s\n' % newJob.user.first_name)
            f.write('Last %s\n' % newJob.user.last_name)
            f.write('Email %s\n' % newJob.user.email)
            f.write('JobName %s\n' % os.path.splitext(os.path.basename(inputFilePath))[0])
            f.write('JobType %s\n' % newJob.jobType)
            f.write('JobExe %s\n' % settings.WL_PATH)
            f.write('JobParameters %s\n' % newJob.jobParameters)
            f.write('OutDir %s\n' % newJob.outdir)
            f.close()

        return newJob

import computation as comp
class hetero_JobForm(forms.Form):
    seq = forms.ModelChoiceField(Sequence.objects.none(), help_text = 'Select sequence to generate PDB Library')

    def __init__(self,user, *args, **kwargs):
        super(hetero_JobForm,self).__init__(*args, **kwargs)
        self.user = user
        #q = Sequence.objects.all()
        q = Sequence.objects.filter(user = self.user)
        self.fields['seq'].queryset = q.extra(order_by = ['tag'])

    def launchJob(self):
        from django.conf import settings
        seqchoice = self.cleaned_data['seq']
        newJob = Sequence_jobs(seq = seqchoice, user = self.user)
        newJob.jobType = 'hetero'
        newJob.jobTypeVerbose = 'PDB Library Generation'
        newJob.jobParameters = '-k %s' % (settings.HETERO_KEY)
        newJob.status = 'launched'
        import os
        from extraFuncs import create_path
        newJob.outdir = os.path.join(settings.DAEMON_OUT_PATH,os.path.normpath("%d/%d/%s/" % (newJob.user.pk, newJob.seq.pk, newJob.jobType)))
        create_path(newJob.outdir)
        seqFilePath = os.path.join(newJob.outdir, 'seq.in')
        comp.Sequence(seqchoice.seq).makeCampariSeqFile(seqFilePath)
        newJob.progressFile = os.path.join(newJob.outdir, 'progress.txt')
        inputFilePath = os.path.normpath("%s/%d_%d_%s" % (settings.DAEMON_IN_PATH, newJob.user.pk, newJob.seq.pk, newJob.jobType))
        create_path(os.path.dirname(inputFilePath))
        if(Sequence_jobs.objects.filter(seq = newJob.seq, jobType = newJob.jobType).exists()):
            newJob.status = 'ar'
            return newJob
        newJob.save()
        with open(inputFilePath, 'w') as f:
            f.write('User %s\n' % newJob.user.username)
            f.write('First %s\n' % newJob.user.first_name)
            f.write('Last %s\n' % newJob.user.last_name)
            f.write('Email %s\n' % newJob.user.email)
            f.write('JobName %s\n' % os.path.splitext(os.path.basename(inputFilePath))[0])
            f.write('JobType %s\n' % newJob.jobType)
            f.write('JobExe %s\n' % settings.CAMPARI_PATH)
            f.write('JobParameters %s\n' % newJob.jobParameters)
            f.write('OutDir %s\n' % newJob.outdir)
            f.close()


        return newJob

class tagForm(forms.Form):
    tag = forms.MultipleChoiceField(choices = [], help_text = 'Filter by sequence tag')
    def __init__(self,user, *args, **kwargs):
        super(tagForm,self).__init__(*args, **kwargs)
        self.user = user
        q = Sequence.objects.filter(user = self.user)
        tagSet = set()
        for possibleSeqs in q:
            tagSet.add(possibleSeqs.tag)
        choiceField = []
        for e in tagSet:
            choiceField.append((e,e,))
        self.fields['tag'].choices = choiceField
        print(choiceField)

class seqForm(forms.Form):
    seqs = forms.ModelMultipleChoiceField(Sequence.objects.none())
    def __init__(self,user, *args, **kwargs):
        super(seqForm,self).__init__(*args, **kwargs)
        self.user = user
        self.help_text = ''

    def fillField(self,tags):
        seqSet = Sequence.objects.none()
        for t in tags:
            seqSet = seqSet | Sequence.objects.filter(tag = t)
        self.fields['seqs'].queryset = seqSet

    def getSeqTable(self):
        try:
            seqlist = self.cleaned_data['seqs']
        except:
            seqlist = Sequence.objects.none()
        seqdata = Sequence_seqdata.objects.select_related().filter(seq = seqlist)
        import django_tables2 as tables
        class SeqDataTable(tables.Table):
            pk = tables.Column(verbose_name = 'sequence id')
            FCR = tables.Column()
            NCPR = tables.Column()
            meanH = tables.Column(verbose_name = '<H>')
            kappa = tables.Column()
            class Meta:
                attrs = {'class': 'pure-table'}
        return SeqDataTable(seqdata)

    def getPhasePlot(self):
        try:
            seqlist = self.cleaned_data['seqs']
        except:
            seqlist = Sequence.objects.none()
        seqdata = Sequence_seqdata.objects.select_related().filter(seq = seqlist)
        fplus = []
        fminus = []
        labels = []
        for s in seqdata:
            fplus.append(s.fplus)
            fminus.append(s.fminus)
            if(s.seq.name == ''):
                labels.append('%d' % (s.pk))
            else:
                labels.append(s.seq.name)
        from django.conf import settings
        import os
        from plotting import phasePlot
        saveDir = os.path.join(settings.STATIC_PATH, os.path.normpath('temp_%s_%s.png' %(self.user.username,'phase')))
        phasePlot(fplus,fminus,labels,saveDir)
        return os.path.basename(saveDir)

