from django.db import models

from core.models import TimeStampModel

class Status(models.Model): 
    status = models.CharField(max_length=45)

    class Meta: 
        db_table = "statuses"

class Application(TimeStampModel): 
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    job    = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    resume = models.ForeignKey('resumes.Resume', on_delete=models.CASCADE)

    class Meta: 
        db_table = "applications"

