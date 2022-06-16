from django.urls import path
from jobs.views  import FollowView, FollowedJobView, JobListPrivateView, RandomJobListView

urlpatterns = [
    path("/<int:job_id>/follow", FollowView.as_view()),
    path("/followedjob", FollowedJobView.as_view()),
    path('/private', JobListPrivateView.as_view()),
    path('/random', RandomJobListView.as_view())
] 