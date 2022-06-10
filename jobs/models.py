from django.db import models

from core.models import TimeStampModel

class MainCategory(models.Model): 
    name = models.CharField(max_length=45)

    class Meta: 
        db_table = "main_categories"

class SubCategory(models.Model): 
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    name          = models.CharField(max_length=45)

    class Meta: 
        db_table = "sub_categories"

class Location(models.Model): 
    name = models.CharField(max_length=45)

    class Meta: 
        db_table = "locations"

class Company(models.Model): 
    name      = models.CharField(max_length=45)
    address   = models.CharField(max_length=200)
    logo      = models.URLField(max_length=500)
    location  = models.ForeignKey('Location', on_delete=models.CASCADE)
    latitude  = models.DecimalField(max_digits= 8, decimal_places=5, null=True)
    longitude = models.DecimalField(max_digits= 8, decimal_places=5, null=True)

    class Meta: 
        db_table = "companies"

class CompanyImage(models.Model): 
    image_url  = models.URLField(max_length=500)
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)

    class Meta: 
        db_table = "company_images"

class Career(models.Model): 
    name = models.CharField(max_length=50)

    class Meta: 
        db_table = "careers"

class Job(models.Model): 
    name         = models.CharField(max_length=50)
    content      = models.TextField()
    due_date     = models.DateField()
    career       = models.ForeignKey('Career', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    company      = models.ForeignKey('Company', on_delete=models.CASCADE)

    class Meta: 
        db_table = "jobs"

class Skill(models.Model): 
    name = models.CharField(max_length=45)

    class Meta: 
        db_table = "skills"

class RequiredSkill(models.Model): 
    job   = models.ForeignKey('Job', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)

    class Meta: 
        db_table = "requiredskills"

class Follow(TimeStampModel): 
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    job  = models.ForeignKey('Job', on_delete=models.CASCADE)
    
    class Meta: 
        db_table = "follows"