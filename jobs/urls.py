from django.urls import path
from jobs.views  import JobDetailView, FollowView, FollowedJobView

urlpatterns = [
    path("/<int:job_id>", JobDetailView.as_view()),
    path("/<int:job_id>/follow", FollowView.as_view()),
    path("/followedjob", FollowedJobView.as_view())
] 