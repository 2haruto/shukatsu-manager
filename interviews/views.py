from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Interview
from .forms import ReflectionItemForm, InterviewForm


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
