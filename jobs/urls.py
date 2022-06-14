from django.urls import path
from jobs.views  import FollowView, FollowedJobView, JobListPublicView, JobListPrivateView

urlpatterns = [
    path("/<int:job_id>/follow", FollowView.as_view()),
    path("/followedjob", FollowedJobView.as_view()),
    path('/public', JobListPublicView.as_view()),
    path('/private', JobListPrivateView.as_view())
] 