from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils import timezone

from companies.models import Company
from interviews.models import Interview, ReflectionItem

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def mypage(request):
    user = request.user

    companies_count = Company.objects.filter(owner=user).count()
    interviews_count = Interview.objects.filter(company__owner=user).count()
    reflections_count = ReflectionItem.objects.filter(interview__company__owner=user).count()

    upcoming = (
        Interview.objects.select_related("company")
        .filter(company__owner=user, scheduled_at__gte=timezone.now())
        .order_by("scheduled_at")[:5]
    )
    recent_reflections = (
        ReflectionItem.objects.select_related("interview__company")
        .filter(interview__company__owner=user)
        .order_by("-created_at")[:5]
    )

    return render(request, "accounts/mypage.html", {
        "companies_count": companies_count,
        "interviews_count": interviews_count,
        "reflections_count": reflections_count,
        "upcoming": upcoming,
        "recent_reflections": recent_reflections,
    })
