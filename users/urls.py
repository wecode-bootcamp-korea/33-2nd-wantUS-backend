from django.urls import path 
from users.views import KakaoSignInView, KakaoCallBackView, GoogleSignInView, GoogleCallBackView

urlpatterns = [
    path("/signin/kakao/callback", KakaoCallBackView.as_view()),
    path("/signin/kakao", KakaoSignInView.as_view()),
    path("/signin/google", GoogleSignInView.as_view()),
    path("/signin/google/callback", GoogleCallBackView.as_view()),
]