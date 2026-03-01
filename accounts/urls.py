from django.urls import path
from .views import signup, mypage, AppLoginView

urlpatterns = [
    path("login/", AppLoginView.as_view(), name="login"),
    path("signup/", signup, name="signup"),
    path("me/", mypage, name="mypage"),
]