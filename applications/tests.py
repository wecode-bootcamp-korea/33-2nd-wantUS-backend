import jwt

from django.test import TestCase, Client
from django.conf import settings

from applications.models import *
from users.models        import *
from jobs.models         import *
from resumes.models      import *

class ApplicationResultTest(TestCase):
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
        Location.objects.create(
            id   = 1,
            name = "서울"
        )
        Company.objects.create(
            id          = 1,
            name        = "위코드",
            address     = "서울시 송파구 오륜동",
            logo        = "https://i.pinimg.com/564x/f6/16/1d/f6161d61d9223223fcad406a632fa828.jpg",
            location_id = 1,
            latitude    = "37.1234",
            longitude   = "123.1234"
        )
        MainCategory.objects.create(
            id   = 1,
            name = "개발"
        )
        SubCategory.objects.create(
            id               = 1,
            name             = "앱 개발자",
            main_category_id = 1,
        )
        Career.objects.create(
            id   = 1,
            name = "신입",
        )
        Job.objects.create(
            id              = 1,
            name            = "위코드 개발자",
            content         = "내용",
            due_date        = "2022-06-30",
            career_id       = 1,
            company_id      = 1,
            sub_category_id = 1
        )
        Resume.objects.create(
            id       = 1,
            name     = "이력서.pdf",
            file_url = "https://jhwang-test-bucket.s3.us-east-2.amazonaws.com/cf3f890cdf6c",
            user_id  = 1
        )
        Status.objects.create(
            id     = 1,
            status = "서류통과",
        )
        Application.objects.create(
            id        = 1,
            job_id    = 1,
            resume_id = 1,
            status_id = 1,
            user_id   = 1
        )
        
        self.token = jwt.encode({"id" : User.objects.get(id=1).id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

    def tearDown(self): 
        User.objects.all().delete()
        Social.objects.all().delete()
        Location.objects.all().delete()
        Company.objects.all().delete()
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Career.objects.all().delete()
        Job.objects.all().delete()
        Resume.objects.all().delete()
        Status.objects.all().delete()
        Application.objects.all().delete()

    def test_application_result_success(self):
        client = Client()
        headers  = {"HTTP_Authorization" : self.token}
        response = client.get("/application/results", **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'application_results': [{
                'company_logo': 'https://i.pinimg.com/564x/f6/16/1d/f6161d61d9223223fcad406a632fa828.jpg',
                'company_name': '위코드',
                'id'          : 1,
                'position'    : '위코드 개발자',
                'result'      : '서류통과',
                'time'        : Resume.objects.get(id=1).updated_at.strftime('%Y.%m.%d')
            }],
            'user_info': {
                'email': 'kim1234@gmail.com',
                'id'   : 1,
                'name' : '김아무개'
            }
        })