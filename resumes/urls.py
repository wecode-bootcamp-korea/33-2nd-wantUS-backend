from django.urls import path
from .views      import ResumeView, ResumeDownloadView, ResumeListView

urlpatterns = [
    path("/upload", ResumeView.as_view()),
    path("/<int:resume_id>/delete", ResumeView.as_view()),
    path("/<int:resume_id>/download", ResumeDownloadView.as_view()),
    path('/list', ResumeListView.as_view()),
]