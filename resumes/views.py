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
            user      = request.user
            file      = request.FILES['resume']
            file_uuid = str(uuid.uuid4())
            file_url  = f"https://abstunator-wantus-resume-bucket.s3.us-west-2.amazonaws.com/{file_uuid}"

            self.s3_client.upload_fileobj(
                file,
                "abstunator-wantus-resume-bucket",
                file_uuid,
                ExtraArgs = {
                    "ContentType" : file.content_type
                }
            )

            Resume.objects.create(
            name     = file.name,
            file_url = file_url,
            user     = user)
            
            return JsonResponse({'message' : 'UPLOAD_SUCCESS'}, status=201) 

        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status=400)


class ResumeView(View):
    s3_client = boto3.client(
                's3',
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
                )
    # 파일 조회 
    @signin_decorator
    def get (self,request,resume_id):

        try: 
            url = Resume.objects.get(id = resume_id).file_url

            return JsonResponse({'message' : url}, status=200)
        
        except Resume.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_RESUME_ID'}, status=404)
    
      # 파일 삭제 
    @signin_decorator
    def delete (self,request,resume_id):
        try: 

            user   = request.user
            resume = Resume.objects.get(id = resume_id)

            if user.id != resume.user.id:
                return JsonResponse({'message' : 'INVALID_USER'}, status=400)

            resume.delete()
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except Resume.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)
