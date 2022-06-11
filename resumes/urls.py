from django.urls import path
from .views      import ResumeFileUploadView, ResumeView

urlpatterns = [
    path('', ResumeFileUploadView.as_view()),
    path('/list/<int:resume_id>', ResumeView.as_view()),
]