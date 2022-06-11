import json

from django.http  import JsonResponse
from django.views import View

from jobs.models import *
from core.utils  import signin_decorator

class JobDetailView(View):
    @signin_decorator
    def get(self, request, job_id):
        try:
            user = request.user
            job  = Job.objects.prefetch_related('company__companyimage_set').get(id=job_id)

            job_detail = {
                "job_id"           : job.id,
                "job_name"         : job.name,
                "job_content"      : job.content,
                "job_deadline"     : job.due_date,
                "company_id"       : job.company.id,
                "company_name"     : job.company.name,
                "company_address"  : job.company.address,
                "company_location" : job.company.location.name,
                "company_logo"     : job.company.logo,
                "company_images"   : [image.image_url for image in job.company.companyimage_set.all()],
                "company_latitude" : job.company.latitude,
                "company_longitude": job.company.longitude,
            }

            user_info = {
                "id"   : user.id,
                "name" : user.name,
                "email": user.email
            }
            
            return JsonResponse({"job_detail" : job_detail, "user_info" : user_info}, status=200)

        except Job.DoesNotExist:
            return JsonResponse({"message" : "JOB_DOES_NOT_EXIST"}, status=404)