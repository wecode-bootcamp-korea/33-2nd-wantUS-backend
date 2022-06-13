from django.urls import path
from jobs.views  import JobDetailView, FollowView

urlpatterns = [
    path("/<int:job_id>", JobDetailView.as_view()),
    path("/<int:job_id>/follow", FollowView.as_view()),
] 