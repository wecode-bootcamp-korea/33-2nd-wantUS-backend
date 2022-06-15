import jwt
import json

from django.test import TestCase, Client
from django.conf import settings

from users.models import *
from jobs.models  import *

class JobDetailTest(TestCase):
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

    def test_job_detail_get_success(self):
        client   = Client()
        headers  = {"HTTP_Authorization" : self.token}
        response = client.get("/job/1", **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_job_detail_get_does_not_exist(self): 
        client   = Client()
        headers  = {"HTTP_Authorization" : self.token}
        response = client.get("/job/2", **headers, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "message": "JOB_DOES_NOT_EXIST",
        })

class FollowTest(TestCase):
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

    def test_follow_success(self): 
        client   = Client()
        headers  = {"HTTP_Authorization" : self.token}
        response = client.post("/job/1/follow", **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message"     : "FOLLOW_SUCCESS",
            "results"     : True,
            "follow_count": 1
        })

    def test_unfollow_success(self): 
        client = Client()
        Follow.objects.create(id=1, job_id=1, user_id=1)
        headers  = {"HTTP_Authorization" : self.token}
        response = client.post("/job/1/follow", **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message"     : "FOLLOW_DELETE",
            "results"     : False,
            "follow_count": 0
        })

class FollowedJobTest(TestCase):
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
        CompanyImage.objects.create(
            id = 1,
            image_url = "https://i.pinimg.com/564x/27/e0/74/27e074008b1d54fb474224de9102651b.jpg",
            company_id_id = 1
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
        CompanyImage.objects.all().delete()

    def test_followed_job_success(self):
        client   = Client()
        headers  = {"HTTP_Authorization" : self.token}
        response = client.get("/job/followedjob", **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
