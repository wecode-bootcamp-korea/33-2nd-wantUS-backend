from django.urls import path
from .views      import ResumeFileUploadView, ResumeView, ResumeListView

urlpatterns = [
    path('/upload', ResumeFileUploadView.as_view()),
    path('/list/<int:resume_id>', ResumeView.as_view()),
    path('/list', ResumeListView.as_view()),
]