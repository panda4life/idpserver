# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 10:59:45 2014

@author: James Ahad
"""

from django import forms

from django.contrib.auth.models import User
from idp.models import UserProfile, Sequence, Sequence_seqdata
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