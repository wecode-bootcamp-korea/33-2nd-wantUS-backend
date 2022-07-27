import json
import jwt

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf                    import settings

from unittest.mock import patch, MagicMock
from users.models  import *


class ResumeUploadTest(TestCase):
    def setUp(self):
        Social.objects.create(
            id   = 2,
            name = 'kakao'
        )
        User.objects.create(
            id                = 1,
            name              = '김아무개',
            profile_image     = 'http://k.kakaocdn.net/dn/eeTOt3/btrtLULVtEZ/5EXNjngEhg1QeAgUE3KKAk/img_640x640.jpg',
            email             = 'kim1234@gmail.com',
            social_account_id = '12345678',
            social_id         = Social.objects.get(name="kakao").id,
        )
        self.token = jwt.encode({"id" : User.objects.get(id=1).id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

    def tearDown(self):
        Social.objects.all().delete()
        User.objects.all().delete()

    @patch('resumes.views.ResumeView.s3_client')
    def test_upload_success(self, mocked_client):

        client = Client()
        headers  = {"HTTP_Authorization" : self.token}

        resume_mock = SimpleUploadedFile('Resume.pdf', b'')

        response = client.post("/resume/upload", {'resume' : resume_mock}, **headers)

        self.assertEqual(response.status_code, 201)