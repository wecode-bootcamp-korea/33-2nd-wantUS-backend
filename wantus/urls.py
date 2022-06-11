from django.urls import path, include

urlpatterns = [
    path('users', include("users.urls")),
    path('jobs', include("jobs.urls")),
    path('applications', include("applications.urls")),
    path('resumes', include("resumes.urls")),
]
