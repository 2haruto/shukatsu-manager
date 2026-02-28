from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .models import Company, School
from .forms import CompanyForm, SchoolForm
from interviews.models import Interview, ReflectionItem, ExamEvent, StudyLog



@login_required
def switch_mode(request, mode: str):
    if mode not in ["job", "student"]:
        mode = "job"
    request.session["mode"] = mode
    return redirect("dashboard")

def home(request):
    return render(request, "home.html")

def build_student_ai_advice(today, weekly_minutes, upcoming_exam_events, recent_study_logs):
    advice = []

    if weekly_minutes == 0:
        advice.append("今週の勉強記録がまだありません。まずは30分だけでも勉強記録を追加して流れを作りましょう。")
    elif weekly_minutes < 180:
        advice.append("今週の勉強時間は少なめです。まずは1日30〜60分を目安に、短くても継続することを優先しましょう。")
    else:
        advice.append("今週はしっかり勉強できています。この調子で継続しつつ、直近イベントの対策を優先しましょう。")

    next_event = upcoming_exam_events.first()
    if next_event:
        advice.append(
            f"直近の予定は「{next_event.title}」です。"
            f"{next_event.school.name}に向けて、関連する科目の復習を先に進めるのがおすすめです。"
        )

    latest_log = recent_study_logs.first()
    if latest_log:
        advice.append(
            f"最近は「{latest_log.get_subject_display()}」を学習しています。"
            f"次は「{latest_log.next_action or '前回の続き'}」を進めると流れが切れにくいです。"
        )
    else:
        advice.append("まだ勉強記録が少ないので、1件目の記録を作って学習の履歴を残していきましょう。")

    return advice[:3]


def build_job_ai_advice(upcoming, recent_reflections):
    advice = []

    next_interview = upcoming.first()
    if next_interview:
        advice.append(
            f"次の面接は「{next_interview.company.name}」の{next_interview.get_stage_display()}面接です。"
            "志望動機・自己紹介・逆質問を先に整理しておくと安心です。"
        )
    else:
        advice.append("直近の面接予定はありません。今のうちに企業研究やESの見直しを進めましょう。")

    latest_reflection = recent_reflections.first()
    if latest_reflection:
        advice.append(
            f"最近の振り返りでは「{latest_reflection.question[:20]}」が記録されています。"
            "前回の改善点を次の面接前に1回見返しておくのがおすすめです。"
        )
    else:
        advice.append("振り返り記録がまだ少ないので、面接ごとに質問・回答・改善点を残していきましょう。")

    advice.append("次回に向けて、結論ファーストで話す練習を1回だけでもやっておくと安定しやすいです。")

    return advice[:3]


@login_required
def dashboard(request):
    mode = request.session.get("mode", "job")

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

    job_ai_advice = build_job_ai_advice(upcoming, recent_reflections)

    context = {
        "mode": mode,
        "upcoming": upcoming,
        "recent_reflections": recent_reflections,
        "job_ai_advice": job_ai_advice,
    }

    if mode == "student":
        today = timezone.localdate()
        start_of_week = today - timedelta(days=today.weekday())

        school_count = School.objects.filter(owner=request.user).count()

        exam_event_count = (
            ExamEvent.objects.select_related("school")
            .filter(school__owner=request.user)
            .count()
        )

        study_log_count = (
            StudyLog.objects.select_related("school")
            .filter(school__owner=request.user)
            .count()
        )

        upcoming_exam_events = (
            ExamEvent.objects.select_related("school")
            .filter(school__owner=request.user, scheduled_at__date__gte=today)
            .order_by("scheduled_at")[:5]
        )

        recent_study_logs = (
            StudyLog.objects.select_related("school")
            .filter(school__owner=request.user)
            .order_by("-study_date", "-created_at")[:5]
        )

        weekly_minutes = (
            StudyLog.objects.filter(
                school__owner=request.user,
                study_date__gte=start_of_week,
                study_date__lte=today,
            ).aggregate(total=Sum("duration_minutes"))["total"]
            or 0
        )

        context.update({
            "school_count": school_count,
            "exam_event_count": exam_event_count,
            "study_log_count": study_log_count,
            "upcoming_exam_events": upcoming_exam_events,
            "recent_study_logs": recent_study_logs,
            "weekly_minutes": weekly_minutes,
            "student_ai_advice": build_student_ai_advice(
                today,
                weekly_minutes,
                upcoming_exam_events,
                recent_study_logs,
            ),
        })

    return render(request, "dashboard.html", context)


@login_required
def company_list(request):
    request.session["mode"] = "job"

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
    request.session["mode"] = "job"

    company = get_object_or_404(Company, pk=pk, owner=request.user)
    interviews = company.interviews.order_by("scheduled_at")
    return render(
        request,
        "companies/company_detail.html",
        {"company": company, "interviews": interviews},
    )


@login_required
def company_create(request):
    request.session["mode"] = "job"

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
    request.session["mode"] = "job"

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
    request.session["mode"] = "job"

    company = get_object_or_404(Company, pk=pk, owner=request.user)

    if request.method == "POST":
        company.delete()
        return redirect("company_list")

    return render(
        request,
        "companies/company_confirm_delete.html",
        {"company": company},
    )


@login_required
def school_list(request):
    request.session["mode"] = "student"

    category = request.GET.get("category", "")
    status = request.GET.get("status", "")
    keyword = request.GET.get("keyword", "").strip()

    schools = School.objects.filter(owner=request.user).order_by("-updated_at")
    total_count = schools.count()

    if category:
        schools = schools.filter(category=category)

    if status:
        schools = schools.filter(status=status)

    if keyword:
        schools = schools.filter(name__icontains=keyword)

    filtered_count = schools.count()

    return render(
        request,
        "companies/school_list.html",
        {
            "schools": schools,
            "keyword": keyword,
            "selected_category": category,
            "selected_status": status,
            "category_choices": School.Category.choices,
            "status_choices": School.Status.choices,
            "total_count": total_count,
            "filtered_count": filtered_count,
        },
    )


@login_required
def school_detail(request, pk: int):
    request.session["mode"] = "student"

    school = get_object_or_404(School, pk=pk, owner=request.user)
    return render(
        request,
        "companies/school_detail.html",
        {"school": school},
    )


@login_required
def school_create(request):
    request.session["mode"] = "student"

    if request.method == "POST":
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save(commit=False)
            school.owner = request.user
            school.save()
            return redirect("school_detail", pk=school.pk)
    else:
        form = SchoolForm()

    return render(
        request,
        "companies/school_form.html",
        {"form": form, "title": "学校追加", "submit_label": "追加"},
    )


@login_required
def school_update(request, pk: int):
    request.session["mode"] = "student"

    school = get_object_or_404(School, pk=pk, owner=request.user)

    if request.method == "POST":
        form = SchoolForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            return redirect("school_detail", pk=school.pk)
    else:
        form = SchoolForm(instance=school)

    return render(
        request,
        "companies/school_form.html",
        {"form": form, "title": "学校編集", "submit_label": "保存"},
    )


@login_required
def school_delete(request, pk: int):
    request.session["mode"] = "student"

    school = get_object_or_404(School, pk=pk, owner=request.user)

    if request.method == "POST":
        school.delete()
        return redirect("school_list")

    return render(
        request,
        "companies/school_confirm_delete.html",
        {"school": school},
    )