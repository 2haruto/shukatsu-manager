from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Company
from interviews.models import Interview, ReflectionItem


@login_required
def dashboard(request):
    upcoming = (
        Interview.objects.select_related("company")
        .filter(company__owner=request.user, scheduled_at__gte=timezone.now())
        .order_by("scheduled_at")[:5]
    )
    recent_reflections = (
        ReflectionItem.objects.select_related("interview__company")
        .filter(interview__company__owner=request.user)
        .order_by("-created_at")[:5]
    )
    return render(
        request,
        "dashboard.html",
        {"upcoming": upcoming, "recent_reflections": recent_reflections},
    )


@login_required
def company_list(request):
    companies = Company.objects.filter(owner=request.user).order_by("-updated_at")
    return render(request, "companies/company_list.html", {"companies": companies})


@login_required
def company_detail(request, pk: int):
    company = get_object_or_404(Company, pk=pk, owner=request.user)
    interviews = company.interviews.order_by("scheduled_at")
    return render(
        request,
        "companies/company_detail.html",
        {"company": company, "interviews": interviews},
    )
