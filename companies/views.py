from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .models import Company
from .forms import CompanyForm
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


@login_required
def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect("company_detail", pk=company.pk)
    else:
        form = CompanyForm()

    return render(
        request,
        "companies/company_form.html",
        {"form": form, "title": "企業追加", "submit_label": "追加"},
    )


@login_required
def company_update(request, pk: int):
    company = get_object_or_404(Company, pk=pk, owner=request.user)

    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect("company_detail", pk=company.pk)
    else:
        form = CompanyForm(instance=company)

    return render(
        request,
        "companies/company_form.html",
        {"form": form, "title": "企業編集", "submit_label": "保存"},
    )