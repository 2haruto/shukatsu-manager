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
    status = request.GET.get("status", "")
    keyword = request.GET.get("keyword", "").strip()
    sort = request.GET.get("sort", "updated_desc")

    companies = Company.objects.filter(owner=request.user)
    total_count = companies.count()

    if status:
        companies = companies.filter(status=status)

    if keyword:
        companies = companies.filter(name__icontains=keyword)

    if sort == "priority_desc":
        companies = companies.order_by("-priority", "-updated_at")
    elif sort == "priority_asc":
        companies = companies.order_by("priority", "-updated_at")
    elif sort == "name_asc":
        companies = companies.order_by("name")
    else:
        companies = companies.order_by("-updated_at")

    filtered_count = companies.count()

    status_choices = Company._meta.get_field("status").choices
    sort_choices = [
        ("updated_desc", "更新日が新しい順"),
        ("priority_desc", "優先度が高い順"),
        ("priority_asc", "優先度が低い順"),
        ("name_asc", "企業名順"),
    ]

    return render(
        request,
        "companies/company_list.html",
        {
            "companies": companies,
            "selected_status": status,
            "keyword": keyword,
            "selected_sort": sort,
            "status_choices": status_choices,
            "sort_choices": sort_choices,
            "total_count": total_count,
            "filtered_count": filtered_count,
        },
    )


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


@login_required
def company_delete(request, pk: int):
    company = get_object_or_404(Company, pk=pk, owner=request.user)

    if request.method == "POST":
        company.delete()
        return redirect("company_list")

    return render(
        request,
        "companies/company_confirm_delete.html",
        {"company": company},
    )