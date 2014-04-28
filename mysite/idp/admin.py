from django.contrib import admin
from idp.models import Sequence, Sequence_seqdata, UserProfile
# Register your models here.

admin.site.register(Sequence)
admin.site.register(Sequence_seqdata)
admin.site.register(UserProfile)