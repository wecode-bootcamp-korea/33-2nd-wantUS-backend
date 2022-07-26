import boto3

from django.views import View
from django.http  import JsonResponse
from django.conf  import settings
from pathlib      import Path

from core.utils     import signin_decorator
from users.models   import User
from resumes.models import Resume

class ResumeView(View):
    s3_client = boto3.client(
        's3', 
        aws_access_key_id     = settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    )

    @signin_decorator
    def post(self, request):
        user = request.user.id
        file = request.FILES['resume']
        if file.name.endswith('.pdf') == False:
            return JsonResponse({"message" : "CAN_ONLY_UPLOAD_PDF"}, status=400)

        file_name = str(file)

        self.s3_client.upload_fileobj(
            file, 
            settings.AWS_STORAGE_BUCKET_NAME, 
            file_name, 
            ExtraArgs = {"ContentType": file.content_type}
        )

        Resume(
            name     = file.name,
            file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}",
            user_id  = user
        ).save()

        return JsonResponse({"message" : "UPLOAD_SUCCESS"}, status=201)

    @signin_decorator
    def delete(self, request, resume_id):
        try:
            user      = request.user
            resume    = Resume.objects.get(id = resume_id)
            file_url  = resume.file_url
            file_name = file_url[54:]

            if resume.user.id !=user:
                return JsonResponse({"message" : "UNAUTHORIZED_USER"}, status=401)

            self.s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_name)
            resume.delete()

            return JsonResponse({"message" : "DELETE_SUCCESS"}, status=200)

        except Resume.DoesNotExist:
            return JsonResponse({"message" : "RESUME_DOES_NOT_EXIST"}, status=404)

class ResumeDownloadView(View):
    
    s3_client = boto3.client(
        's3', 
        aws_access_key_id     = settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    )
    @signin_decorator
    def get(self, request, resume_id):
        try:
            user      = request.user
            resume    = Resume.objects.get(id=resume_id)
            file_name = resume.file_url[54:]

            if resume.user.id != user:
                return JsonResponse({"message" : "UNAUTHORIZED_USER"}, status=401)

            self.s3_client.download_file(
                settings.AWS_STORAGE_BUCKET_NAME,
                file_name,
                str(Path.home() / f"Downloads/{file_name}"),
            )

            return JsonResponse({"message" : "DOWNLOAD_SUCCESS"}, status=200)

        except Resume.DoesNotExist:
            return JsonResponse({"message" : "RESUME_DOES_NOT_EXIST"}, status=404)
    
class ResumeListView(View):
    @signin_decorator
    def get(self, request):

        results = [{
            "id"          : resume.id,
            "user"        : resume.user.name,
            "name"        : resume.name,
            "created_date": resume.created_at.strftime('%Y.%m.%d')
        } for resume in Resume.objects.filter(user=request.user)]

        return JsonResponse({"result" : results}, status=200)