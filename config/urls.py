from django.contrib import admin
from django.urls import path, include
from companies.views import home, dashboard, switch_mode

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),

    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("mode/<str:mode>/", switch_mode, name="switch_mode"),

    path("companies/", include("companies.urls")),
    path("interviews/", include("interviews.urls")),
]