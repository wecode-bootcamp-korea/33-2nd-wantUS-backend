import json, uuid, boto3

from django.http  import JsonResponse, HttpResponse
from django.views import View

from resumes.models import Resume
from my_settings    import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from core.utils     import signin_decorator

class ResumeFileUploadView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    @signin_decorator
    def post (self, request):
        try:
            user = request.user
            file = request.FILES['resume']
            key  = str(uuid.uuid4())

            self.s3_client.upload_fileobj(
                file,
                "abstunator-wantus-resume-bucket",
                key,
                ExtraArgs = {
                    "ContentType" : file.content_type
                }
            )

            Resume.objects.create(
                name     = file.name,
                file_url = key,
                user     = user
            )

            return JsonResponse({'message' : 'UPLOAD_SUCCESS'}, status=201) 

        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status=400)

class ResumeView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    
    @signin_decorator
    def delete (self,request, resume_id):
        try:

            resume    = Resume.objects.get(id=resume_id)
            key       = resume.file_url 
            s3_client = boto3.client(
                's3',
                aws_access_key_id     = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            )
            s3_client.delete_object(Bucket='abstunator-wantus-resume-bucket', Key=key)
            resume.delete()

            return HttpResponse(204)

        except Resume.DoesNotExist:
            return JsonResponse({'message' : 'BAD_REQUEST'}, status=404)
    
# 파일 리스트
class ResumeListView(View):
    @signin_decorator
    def get(self, request):

        results = [{
            "id" : resume.id,
            "user" : resume.user.name,
            "name"        : resume.name,
            "created_date": resume.created_at.strftime('%Y.%m.%d')
        } for resume in Resume.objects.filter(user=request.user)]

        return JsonResponse({"result" : results}, status=200)