from django.urls import path 
from applications.views import ApplicationResultView

urlpatterns = [
    path("/results", ApplicationResultView.as_view()),
]