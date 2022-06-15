import json, boto3, uuid

from django.http  import JsonResponse
from django.views import View

from resumes.models import Resume
from my_settings    import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from core.utils     import signin_decorator

# 파일 업로드
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