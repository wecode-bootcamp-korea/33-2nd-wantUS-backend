from django.urls import path
from jobs.views import JobDetailView

urlpatterns = [
    path("/<int:job_id>", JobDetailView.as_view()),
]