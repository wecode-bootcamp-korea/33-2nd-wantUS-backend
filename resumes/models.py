from django.db import models

from core.models import TimeStampModel

class Resume(TimeStampModel):
    name     = models.CharField(max_length=50)
    file_url = models.URLField(max_length=300)
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'resumes'