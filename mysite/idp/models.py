from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    # Base User model provides:
    # username, password, email, firstname, surname
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    jobDir = models.FilePathField(allow_files=False, allow_folders=True) #Points to directory where jobs are running

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class Sequence(models.Model):
    seq = models.CharField(max_length=512, db_index=False)
    tag = models.CharField(max_length=128)
    user = models.ForeignKey(User)
    submissionDate = models.DateField(default = '1900-01-01')
    seqProc = models.BooleanField(default = 0) #Boolean that determines whether the sequence had its parameters solved and stored
    jobProc = models.BooleanField(default = 0) #Boolean that determines whether there are jobs currently running
    class Meta:
        unique_together = (('user', 'seq'),)
    def __unicode__(self):
        return self.seq

class Sequence_seqdata(models.Model):
    seq = models.OneToOneField(Sequence)
    fplus = models.FloatField(default=0)
    fminus = models.FloatField(default=0)
    FCR = models.FloatField(default=0)
    NCPR = models.FloatField(default=0)
    meanH = models.FloatField(default=0)
    #meanCumH = models.CommaSeparatedIntegerField()
    sigma = models.FloatField(default=0)
    delta = models.FloatField(default=0)
    dmax = models.FloatField(default=0)
    kappa = models.FloatField(default=0)
'''
class Sequence_jobdata(models.Model):
    seq = models.ManyToOneField(Sequence)
    jobType = models.IntegerField(default=0)
    jobID = models.IntegerField(default=0)
'''