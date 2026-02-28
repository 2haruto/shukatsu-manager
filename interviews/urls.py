from django.urls import path
from . import views

urlpatterns = [
    path("", views.interview_list, name="interview_list"),
    path("new/", views.interview_create, name="interview_create"),

    path("exam-events/", views.exam_event_list, name="exam_event_list"),
    path("exam-events/new/", views.exam_event_create, name="exam_event_create"),
    path("exam-events/<int:pk>/edit/", views.exam_event_update, name="exam_event_update"),
    path("exam-events/<int:pk>/delete/", views.exam_event_delete, name="exam_event_delete"),
    path("exam-events/<int:pk>/", views.exam_event_detail, name="exam_event_detail"),

    path("study-logs/", views.study_log_list, name="study_log_list"),
    path("study-logs/new/", views.study_log_create, name="study_log_create"),
    path("study-logs/<int:pk>/edit/", views.study_log_update, name="study_log_update"),
    path("study-logs/<int:pk>/delete/", views.study_log_delete, name="study_log_delete"),
    path("study-logs/<int:pk>/", views.study_log_detail, name="study_log_detail"),

    path("<int:pk>/", views.interview_detail, name="interview_detail"),
]