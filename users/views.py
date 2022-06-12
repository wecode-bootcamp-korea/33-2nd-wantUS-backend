import jwt
import requests

from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from django.conf import settings

from users.models import User,Social

class KakaoCallBackView(View):
    def get(self, request):
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type"  : "authorization_code",
            "client_id"   : settings.KAKAO_CLIENT_ID,
            "redirect_uri": "http://localhost:3000/KakaoCallback",
            "code"        : request.GET.get("code")
        }

        access_token = requests.post(kakao_token_api, data=data).json().get('access_token')
        user_info    = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f"Bearer {access_token}"}).json()

        kakao_id          = user_info["id"]
        kakao_name        = user_info["properties"]["nickname"]
        kakao_email       = user_info["kakao_account"]["email"]
        profile_image_url = user_info["properties"]["profile_image"]

        user, is_created = User.objects.get_or_create(
            social_account_id = kakao_id,
            defaults = {
                "name"         : kakao_name,
                "email"        : kakao_email,
                "profile_image": profile_image_url,
                "social_id"    : Social.objects.get(name="kakao").id
            }
        )
        access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

        if is_created:
            return JsonResponse({"message" : "ACCOUNT CREATED", "token" : access_token}, status=201)
        else:
            return JsonResponse({"message" : "SIGN IN SUCCESS", "token" : access_token}, status=200)

class GoogleCallBackView(View):
    def get(self, request):
        google_token_api = "https://oauth2.googleapis.com/token"
        data = {
            "code"         : request.GET.get("code"),
            "client_id"    : settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri" : "http://localhost:3000/GoogleCallback",
            "grant_type"   : "authorization_code"
        }

        access_token = requests.post(google_token_api, data=data).json()['access_token']
        req_uri      = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers      = {'Authorization': f'Bearer {access_token}'}

        user_info        = requests.get(req_uri, headers=headers).json()
        google_id        = user_info["sub"]
        google_name      = user_info["name"]
        google_email     = user_info["email"]
        google_image_url = user_info["picture"]

        user, is_created = User.objects.get_or_create(
            social_account_id = google_id,
            defaults = {
                "name"         : google_name,
                "email"        : google_email,
                "profile_image": google_image_url,
                "social_id"    : Social.objects.get(name="google").id
            }
        )
        access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

        if is_created:
            return JsonResponse({"message" : "ACCOUNT CREATED", "token" : access_token}, status=201)
        else:
            return JsonResponse({"message" : "SIGN IN SUCCESS", "token" : access_token}, status=200)

class NaverCallBackView(View):
    def get(self, request):
        naver_token_api = "https://nid.naver.com/oauth2.0/token"
        data = {
            "code"         : request.GET.get("code"),
            "state"        : request.GET.get("state"),
            "client_id"    : settings.NAVER_CLIENT_ID,
            "client_secret": settings.NAVER_CLIENT_SECRET,
            "grant_type"   : "authorization_code"
        }

        access_token = requests.post(naver_token_api, data=data).json()['access_token']
        req_uri      = 'https://openapi.naver.com/v1/nid/me'
        headers      = {'Authorization': f'Bearer {access_token}'}

        user_info       = requests.get(req_uri, headers=headers).json()
        naver_id        = user_info["response"]["id"]
        naver_name      = user_info["response"]["name"]
        naver_email     = user_info["response"]["email"]
        naver_image_url = user_info["response"]["profile_image"]

        user, is_created = User.objects.get_or_create(
            social_account_id = naver_id,
            defaults = {
                "name"         : naver_name,
                "email"        : naver_email,
                "profile_image": naver_image_url,
                "social_id"    : Social.objects.get(name="naver").id
            }
        )
        access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

        if is_created:
            return JsonResponse({"message" : "ACCOUNT CREATED", "token" : access_token}, status=201)
        else:
            return JsonResponse({"message" : "SIGN IN SUCCESS", "token" : access_token}, status=200)