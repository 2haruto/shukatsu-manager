from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from companies.models import School
from .models import Interview, ExamEvent, StudyLog
from .forms import ReflectionItemForm, InterviewForm, ExamEventForm, StudyLogForm


@login_required
def interview_list(request):
    interviews = (
        Interview.objects.select_related("company")
        .filter(company__owner=request.user)
        .order_by("scheduled_at")
    )
    return render(request, "interviews/interview_list.html", {"interviews": interviews})


@login_required
def interview_detail(request, pk: int):
    interview = get_object_or_404(
        Interview.objects.select_related("company"),
        pk=pk,
        company__owner=request.user,
    )

    if request.method == "POST":
        form = ReflectionItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.interview = interview
            item.save()
            return redirect("interview_detail", pk=interview.pk)
    else:
        form = ReflectionItemForm()

    items = interview.reflection_items.order_by("-created_at")
    return render(
        request,
        "interviews/interview_detail.html",
        {"interview": interview, "items": items, "form": form},
    )


@login_required
def interview_create(request):
    if request.method == "POST":
        form = InterviewForm(request.POST, user=request.user)
        if form.is_valid():
            interview = form.save()
            return redirect("interview_detail", pk=interview.pk)
    else:
        form = InterviewForm(user=request.user)

    return render(request, "interviews/interview_form.html", {"form": form})


@login_required
def interview_list(request):
    interviews = (
        Interview.objects.select_related("company")
        .filter(company__owner=request.user)
        .order_by("scheduled_at")
    )
    return render(request, "interviews/interview_list.html", {"interviews": interviews})


@login_required
def interview_detail(request, pk: int):
    interview = get_object_or_404(
        Interview.objects.select_related("company"),
        pk=pk,
        company__owner=request.user,
    )

    if request.method == "POST":
        form = ReflectionItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.interview = interview
            item.save()
            return redirect("interview_detail", pk=interview.pk)
    else:
        form = ReflectionItemForm()

    items = interview.reflection_items.order_by("-created_at")
    return render(
        request,
        "interviews/interview_detail.html",
        {"interview": interview, "items": items, "form": form},
    )


@login_required
def interview_create(request):
    if request.method == "POST":
        form = InterviewForm(request.POST, user=request.user)
        if form.is_valid():
            interview = form.save()
            return redirect("interview_detail", pk=interview.pk)
    else:
        form = InterviewForm(user=request.user)

    return render(request, "interviews/interview_form.html", {"form": form})


@login_required
def exam_event_list(request):
    event_type = request.GET.get("event_type", "")
    school_id = request.GET.get("school", "")

    exam_events = (
        ExamEvent.objects.select_related("school")
        .filter(school__owner=request.user)
        .order_by("scheduled_at")
    )
    total_count = exam_events.count()

    if event_type:
        exam_events = exam_events.filter(event_type=event_type)

    if school_id:
        exam_events = exam_events.filter(school_id=school_id)

    filtered_count = exam_events.count()
    schools = School.objects.filter(owner=request.user).order_by("name")

    return render(
        request,
        "interviews/exam_event_list.html",
        {
            "exam_events": exam_events,
            "event_type_choices": ExamEvent.EventType.choices,
            "selected_event_type": event_type,
            "schools": schools,
            "selected_school": school_id,
            "total_count": total_count,
            "filtered_count": filtered_count,
        },
    )


@login_required
def exam_event_detail(request, pk: int):
    exam_event = get_object_or_404(
        ExamEvent.objects.select_related("school"),
        pk=pk,
        school__owner=request.user,
    )
    return render(
        request,
        "interviews/exam_event_detail.html",
        {"exam_event": exam_event},
    )


@login_required
def exam_event_create(request):
    initial = {}
    school_id = request.GET.get("school")

    if school_id:
        school = School.objects.filter(pk=school_id, owner=request.user).first()
        if school:
            initial["school"] = school

    if request.method == "POST":
        form = ExamEventForm(request.POST, user=request.user)
        if form.is_valid():
            exam_event = form.save()
            return redirect("exam_event_detail", pk=exam_event.pk)
    else:
        form = ExamEventForm(user=request.user, initial=initial)

    return render(
        request,
        "interviews/exam_event_form.html",
        {"form": form, "title": "受験イベント追加", "submit_label": "追加"},
    )


@login_required
def exam_event_update(request, pk: int):
    exam_event = get_object_or_404(
        ExamEvent.objects.select_related("school"),
        pk=pk,
        school__owner=request.user,
    )

    if request.method == "POST":
        form = ExamEventForm(request.POST, instance=exam_event, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("exam_event_detail", pk=exam_event.pk)
    else:
        form = ExamEventForm(instance=exam_event, user=request.user)

    return render(
        request,
        "interviews/exam_event_form.html",
        {"form": form, "title": "受験イベント編集", "submit_label": "保存"},
    )


@login_required
def exam_event_delete(request, pk: int):
    exam_event = get_object_or_404(
        ExamEvent.objects.select_related("school"),
        pk=pk,
        school__owner=request.user,
    )

    if request.method == "POST":
        exam_event.delete()
        return redirect("exam_event_list")

    return render(
        request,
        "interviews/exam_event_confirm_delete.html",
        {"exam_event": exam_event},
    )


@login_required
def study_log_list(request):
    subject = request.GET.get("subject", "")
    school_id = request.GET.get("school", "")

    study_logs = (
        StudyLog.objects.select_related("school")
        .filter(school__owner=request.user)
        .order_by("-study_date", "-created_at")
    )
    total_count = study_logs.count()

    if subject:
        study_logs = study_logs.filter(subject=subject)

    if school_id:
        study_logs = study_logs.filter(school_id=school_id)

    filtered_count = study_logs.count()
    schools = School.objects.filter(owner=request.user).order_by("name")

    return render(
        request,
        "interviews/study_log_list.html",
        {
            "study_logs": study_logs,
            "subject_choices": StudyLog.Subject.choices,
            "selected_subject": subject,
            "schools": schools,
            "selected_school": school_id,
            "total_count": total_count,
            "filtered_count": filtered_count,
        },
    )


@login_required
def study_log_detail(request, pk: int):
    study_log = get_object_or_404(
        StudyLog.objects.select_related("school"),
        pk=pk,
        school__owner=request.user,
    )
    return render(
        request,
        "interviews/study_log_detail.html",
        {"study_log": study_log},
    )


@login_required
def study_log_create(request):
    initial = {}
    school_id = request.GET.get("school")

    if school_id:
        school = School.objects.filter(pk=school_id, owner=request.user).first()
        if school:
            initial["school"] = school

    if request.method == "POST":
        form = StudyLogForm(request.POST, user=request.user)
        if form.is_valid():
            study_log = form.save()
            return redirect("study_log_detail", pk=study_log.pk)
    else:
        form = StudyLogForm(user=request.user, initial=initial)

    return render(
        request,
        "interviews/study_log_form.html",
        {"form": form, "title": "勉強記録追加", "submit_label": "追加"},
    )


@login_required
def study_log_update(request, pk: int):
    study_log = get_object_or_404(
        StudyLog.objects.select_related("school"),
        pk=pk,
        school__owner=request.user,
    )

    if request.method == "POST":
        form = StudyLogForm(request.POST, instance=study_log, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("study_log_detail", pk=study_log.pk)
    else:
        form = StudyLogForm(instance=study_log, user=request.user)

    return render(
        request,
        "interviews/study_log_form.html",
        {"form": form, "title": "勉強記録編集", "submit_label": "保存"},
    )


@login_required
def study_log_delete(request, pk: int):
    study_log = get_object_or_404(
        StudyLog.objects.select_related("school"),
        pk=pk,
        school__owner=request.user,
    )

    if request.method == "POST":
        study_log.delete()
        return redirect("study_log_list")

    return render(
        request,
        "interviews/study_log_confirm_delete.html",
        {"study_log": study_log},
    )