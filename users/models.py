from django.db import models

from core.models import TimeStampModel

class Social(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "socials"

class User(TimeStampModel):
    name              = models.CharField(max_length=45)
    contact           = models.CharField(max_length=45)
    profile_image     = models.CharField(max_length=500)
    email             = models.CharField(max_length=50, unique=True)
    social            = models.ForeignKey('Social', on_delete=models.CASCADE)
    social_account_id = models.CharField(max_length=200)
    terms_agreements  = models.JSONField()

    class Meta:
        db_table = "users"
