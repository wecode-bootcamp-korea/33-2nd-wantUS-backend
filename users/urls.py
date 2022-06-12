from django.urls import path 
from users.views import KakaoCallBackView, GoogleCallBackView, NaverCallBackView

urlpatterns = [
    path("/signin/kakao/callback", KakaoCallBackView.as_view()),
    path("/signin/google/callback", GoogleCallBackView.as_view()),
    path("/signin/naver/callback", NaverCallBackView.as_view()),
]