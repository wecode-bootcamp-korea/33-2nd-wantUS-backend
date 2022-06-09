import json
import jwt
import requests

from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from django.conf import settings

from users.models import User,Social

class KakaoSignInView(View):
    def get(self, request):
        client_id     = settings.KAKAO_CLIENT_ID
        kakao_auth_id = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri  = "http://localhost:8000/user/signin/kakao/callback"

        return redirect(
            f"{kakao_auth_id}&client_id={client_id}&redirect_uri={redirect_uri}"
            )

class KakaoCallBackView(View):
    def get(self, request):
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type"  : "authorization_code",
            "client_id"   : settings.KAKAO_CLIENT_ID,
            "redirect_uri": "http://localhost:8000/user/signin/kakao/callback",
            "code"        : request.GET.get("code")
        }

        access_token = requests.post(kakao_token_api, data=data).json().get('access_token')
        user_info    = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f"Bearer {access_token}"}).json()

        kakao_id          = user_info["id"]
        kakao_name        = user_info["properties"]["nickname"]
        kakao_email       = user_info["kakao_account"]["email"]
        profile_image_url = user_info["properties"]["profile_image"]

        if User.objects.filter(social_account_id = kakao_id).exists():
            user = User.objects.get(social_account_id = kakao_id)
            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({"message" : "SIGN IN SUCCESS", "token" : access_token}, status=200)
        
        User(
            social_account_id = kakao_id,
            name              = kakao_name,
            email             = kakao_email,
            profile_image     = profile_image_url,
            social_id         = Social.objects.get(name="kakao").id,
        ).save()

        user = User.objects.get(social_account_id=kakao_id)
        access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
        
        return JsonResponse({"message" : "ACCOUNT CREATED", "token" : access_token}, status=201)

class GoogleSignInView(View):
    def get(self, request):
        client_id       = settings.GOOGLE_CLIENT_ID
        redirect_uri    = "http://localhost:8000/user/signin/google/callback"
        scope           = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
        google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"

        return redirect(
            f"{google_auth_api}?scope={scope}&response_type=code&redirect_uri={redirect_uri}&client_id={client_id}"
        )

class GoogleCallBackView(View):
    def get(self, request):
        google_token_api = "https://oauth2.googleapis.com/token"
        data = {
            "code" : request.GET.get("code"),
            "client_id" : settings.GOOGLE_CLIENT_ID,
            "client_secret" : settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri" : "http://localhost:8000/user/signin/google/callback",
            "grant_type" : "authorization_code"
        }

        access_token = requests.post(google_token_api, data=data).json()['access_token']
        req_uri      = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers      = {'Authorization': f'Bearer {access_token}'}

        user_info        = requests.get(req_uri, headers=headers).json()
        google_id        = user_info["sub"]
        google_name      = user_info["name"]
        google_email     = user_info["email"]
        google_image_url = user_info["picture"]

        if User.objects.filter(social_account_id = google_id).exists():
            user         = User.objects.get(social_account_id = google_id)
            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({"message" : "SIGN IN SUCCESS", "token" : access_token}, status=200)
        
        User(
            social_account_id = google_id,
            name              = google_name,
            email             = google_email,
            profile_image     = google_image_url,
            social_id         = Social.objects.get(name="google").id,
        ).save()

        user         = User.objects.get(social_account_id=google_id)
        access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
        
        return JsonResponse({"message" : "ACCOUNT CREATED", "token" : access_token}, status=201)
