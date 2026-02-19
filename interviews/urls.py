from django.urls import path
from . import views

urlpatterns = [
    path("", views.interview_list, name="interview_list"),
    path("new/", views.interview_create, name="interview_create"),
    path("<int:pk>/", views.interview_detail, name="interview_detail"),
]
