from django.urls import path
from .views import signup, mypage

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("me/", mypage, name="mypage"),
]
