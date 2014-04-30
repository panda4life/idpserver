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
    name = models.CharField(max_length=128, default = '')
    tag = models.CharField(max_length=128)
    user = models.ForeignKey(User)
    submissionDate = models.DateField(default = '1900-01-01')
    seqProc = models.BooleanField(default = 0) #Boolean that determines whether the sequence had its parameters solved and stored
    jobProc = models.BooleanField(default = 0) #Boolean that determines whether there are jobs currently running
    class Meta:
        unique_together = (('user', 'seq'),('tag','name'))
    def __unicode__(self):
        if(self.name == ''):
            return self.seq
        return self.name

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
    def __unicode__(self):
        return self.seq.__unicode__()

class Sequence_jobs(models.Model):
    seq = models.ForeignKey(Sequence)
    user = models.ForeignKey(User)
    jobType = models.CharField(max_length = 128, default = '')
    jobParameters = models.CharField(max_length = 1024, )
    status = models.CharField(max_length = 2, default = 'l')
    progressFile = models.FilePathField(max_length = 512, default = '/output/progress.txt')
    outdir = models.FilePathField(max_length = 512, default = '/output/',allow_folders = True, allow_files = False)

'''
class Sequence_jobdata(models.Model):
    seq = models.ManyToOneField(Sequence)
    jobType = models.IntegerField(default=0)
    jobID = models.IntegerField(default=0)
'''