from django.urls import path
from . import views

urlpatterns = [
    path("", views.interview_list, name="interview_list"),
    path("<int:pk>/", views.interview_detail, name="interview_detail"),
]
