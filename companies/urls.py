from django.urls import path
from . import views

urlpatterns = [
    path("", views.company_list, name="company_list"),
    path("new/", views.company_create, name="company_create"),

    path("schools/", views.school_list, name="school_list"),
    path("schools/new/", views.school_create, name="school_create"),
    path("schools/<int:pk>/edit/", views.school_update, name="school_update"),
    path("schools/<int:pk>/delete/", views.school_delete, name="school_delete"),
    path("schools/<int:pk>/", views.school_detail, name="school_detail"),

    path("<int:pk>/edit/", views.company_update, name="company_update"),
    path("<int:pk>/delete/", views.company_delete, name="company_delete"),
    path("<int:pk>/", views.company_detail, name="company_detail"),
]