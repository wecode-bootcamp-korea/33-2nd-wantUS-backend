from django.urls import path
from .views      import ResumeFileUploadView

urlpatterns = [
    path('', ResumeFileUploadView.as_view()),
]