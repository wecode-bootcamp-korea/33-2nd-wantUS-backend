from django.urls import path 
from .views      import ResumeView

urlpatterns = [
    path('/list/<int:resume_id>', ResumeView.as_view()),
]


