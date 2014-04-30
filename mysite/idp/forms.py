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
        return self.user

class MultiSequenceForm(forms.Form):
    seqlist = forms.CharField(widget=forms.Textarea, help_text = "Please enter amino acid sequences separated by carraige returns")
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
            newSequence = Sequence(seq = seqstring,
                                   tag = self.cleaned_data['tag'],
                                   user = self.user,
                                   submissionDate = timezone.now(),
                                   seqProc = False,
                                   jobProc = False,)
            newSequence.save()
            newSeqData = Sequence_seqdata(seq = newSequence,
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
        if(self.cleaned_data['genPermutants']):
            newJob.jobType = 'wlp'
            newJob.jobParameters = ''
        else:
            newJob.jobType = 'wl'
            newJob.jobParameters = ''
        newJob.status = 'l'
        import os
        from django.conf import settings
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
            f.write('JobID %d\n' % newJob.pk)
            f.write('UserID %d\n' % newJob.user.pk)
            f.write('JobType %s\n' % newJob.pk)
            f.write('JobParameters %s\n' % newJob.jobParameters)
            f.write('OutDir %s\n' % newJob.outdir)
            f.close()

        return newJob

class hetero_JobForm(forms.Form):
    seq = forms.ModelChoiceField(Sequence.objects.none(), help_text = 'Select sequence to generate PDB Library')

    def __init__(self,user, *args, **kwargs):
        super(hetero_JobForm,self).__init__(*args, **kwargs)
        self.user = user
        #q = Sequence.objects.all()
        q = Sequence.objects.filter(user = self.user)
        self.fields['seq'].queryset = q.extra(order_by = ['tag'])

    def launchJob(self):
        seqchoice = self.cleaned_data['seq']
        newJob = Sequence_jobs(seq = seqchoice, user = self.user)
        newJob.jobType = 'hetero'
        newJob.jobParameters = 'hetero'
        newJob.status = 'l'
        import os
        from django.conf import settings
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
            f.write('JobID %d\n' % newJob.pk)
            f.write('UserID %d\n' % newJob.user.pk)
            f.write('JobType %s\n' % newJob.pk)
            f.write('JobParameters %s\n' % newJob.jobParameters)
            f.write('OutDir %s\n' % newJob.outdir)
            f.close()

        return newJob

class tagForm(forms.Form):
    tag = forms.MultipleChoiceField(choices = None)
    def __init__(self,user, *args, **kwargs):
        super(tagForm,self).__init__(*args, **kwargs)
        self.user = user
        q = Sequence.objects.filter(user = self.user)
        tagSet = set()
        for possibleSeqs in q:
            tagSet.add(possibleSeqs.tag)
        self.fields['tag'].queryset = tagSet