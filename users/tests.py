import jwt

from django.test import TestCase, Client
from django.conf import settings
from unittest import mock
from unittest.mock import patch

from users.models import *

class KakaoSignInTest(TestCase):
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
            terms_agreements  = {1:2},
            social_id         = Social.objects.get(name="kakao").id,
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_success_kakao_new_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self): 
                return {
                    "id"          : 12341234,
                    "connected_at": "2022-06-08T01:29:52Z",
                    "properties"  : {
                        "nickname"       : "홍길동",
                        "profile_image"  : "http://k.kakaocdn.net/dn/eeTOt3/btrtLULVtEZ/5EXNjngEhg1QeAgUE3KKAk/img_640x640.jpg",
                        "thumbnail_image": "http://k.kakaocdn.net/dn/eeTOt3/btrtLULVtEZ/5EXNjngEhg1QeAgUE3KKAk/img_110x110.jpg"
                    },
                    "kakao_account": {
                        "profile_nickname_needs_agreement": False,
                        "profile_image_needs_agreement"   : False,
                        "profile"                         : {
                            "nickname"           : "홍길동",
                            "thumbnail_image_url": "http://k.kakaocdn.net/dn/eeTOt3/btrtLULVtEZ/5EXNjngEhg1QeAgUE3KKAk/img_110x110.jpg",
                            "profile_image_url"  : "http://k.kakaocdn.net/dn/eeTOt3/btrtLULVtEZ/5EXNjngEhg1QeAgUE3KKAk/img_640x640.jpg",
                            "is_default_image"   : False
                            },
                        "has_email"            : True,
                        "email_needs_agreement": False,
                        "is_email_valid"       : True,
                        "is_email_verified"    : True,
                        "email"                : "hong123@gmail.com"
                    }
                }

        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "12341234"}
        response            = client.get("/user/signin/kakao/callback", **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'message': 'ACCOUNT CREATED',
            'token'  : jwt.encode({'id': User.objects.latest('id').id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        })        

    @patch("users.views.requests")
    def test_success_kakao_existed_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id"          : 12345678,
                    "connected_at": "2022-06-08T01:29:52Z",
                    "properties"  : {
                        "nickname"       : "김아무개",
                        "profile_image"  : "http://k.kakaocdn.net/dn/eeTOt3/btrtLULVtEZ/5EXNjngEhg1QeAgUE3KKAk/img_640x640.jpg",
                        "thumbnail_image": "http://k.kakaocdn.net/dn/eeTOt3/btrtLULVtEZ/5EXNjngEhg1QeAgUE3KKAk/img_110x110.jpg"
                    },
                    "kakao_account": {
                        "profile_nickname_needs_agreement": False,
                        "profile_image_needs_agreement"   : False,
                        "profile"                         : {
                            "nickname"           : "김아무개",
                            "thumbnail_image_url": "http://k.kakaocdn.net/dn/eeTOt3/btrtLULVtEZ/5EXNjngEhg1QeAgUE3KKAk/img_110x110.jpg",
                            "profile_image_url"  : "http://k.kakaocdn.net/dn/eeTOt3/btrtLULVtEZ/5EXNjngEhg1QeAgUE3KKAk/img_640x640.jpg",
                            "is_default_image"   : False
                            },
                        "has_email"            : True,
                        "email_needs_agreement": False,
                        "is_email_valid"       : True,
                        "is_email_verified"    : True,
                        "email"                : "Kim1234@gmail.com"
                    }
                }

        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "12345678"}
        response            = client.get("/user/signin/kakao/callback", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message': 'SIGN IN SUCCESS',
            'token'  : jwt.encode({'id': User.objects.latest('id').id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        })

class GoogleSignInTest(TestCase):
    def setUp(self): 
        Social.objects.create(
            id   = 1,
            name = 'google'
        )
        User.objects.create(
            id                = 1,
            name              = '황재승',
            profile_image     = 'https://lh3.googleusercontent.com/a/AATXAJyJ31Yj38kTInJgJ4ducCl6Wx-QlX49FzQh0kF9=s96-c',
            email             = 'gogolee@gmail.com',
            social_account_id = '5544332211',
            terms_agreements  = {1:2},
            social_id         = Social.objects.get(name="google").id,
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_success_google_new_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "sub"           : "1122334455",
                    "name"          : "\ud669\uc7ac\uc2b9",
                    "given_name"    : "\uc7ac\uc2b9",
                    "family_name"   : "\ud669",
                    "picture"       : "https://lh3.googleusercontent.com/a/AFFEASSSXXDFAEucCl6Wx-QlX49FzQh0kF9=s96-c",
                    "email"         : "lululala@gmail.com",
                    "email_verified": True,
                    "locale"        : "ko"
                    }

        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "11223344"}
        response            = client.get("/user/signin/google/callback", **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'message': 'ACCOUNT CREATED',
            'token'  : jwt.encode({'id': User.objects.latest('id').id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        })     

    @patch("users.views.requests")
    def test_success_kakao_existed_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "sub"           : "5544332211",
                    "name"          : "\ud669\uc7ac\uc2b9",
                    "given_name"    : "\uc7ac\uc2b9",
                    "family_name"   : "\ud669",
                    "picture"       : "https://lh3.googleusercontent.com/a/AATXAJyJ31Yj38kTInJgJ4ducCl6Wx-QlX49FzQh0kF9=s96-c",
                    "email"         : "gogolee@gmail.com",
                    "email_verified": True,
                    "locale"        : "ko"
                    }

        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers = {"HTTP_Authorization" : "12345678"}
        response = client.get("/user/signin/google/callback", **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message': 'SIGN IN SUCCESS', 
            'token': jwt.encode({'id': User.objects.latest('id').id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        })