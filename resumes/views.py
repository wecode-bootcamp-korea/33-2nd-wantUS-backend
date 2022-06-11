from django.shortcuts import render

import boto3

from django.http    import JsonResponse
from django.views   import View

from resumes.models import Resume
from my_settings    import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from core.utils     import signin_decorator

# 파일 조회 
class ResumeView(View):
    s3_client = boto3.client(
                's3',
                aws_access_key_id     = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
                )
    @signin_decorator
    def get (self,request,resume_id):

        try: 
            url = Resume.objects.get(id = resume_id).file_url

            return JsonResponse({'message' : url}, status=200)
        
        except Resume.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_RESUME_ID'}, status=404)