from django.db import models
from companies.models import Company, School


class Interview(models.Model):
    class Stage(models.TextChoices):
        CASUAL = "casual", "カジュアル"
        FIRST = "first", "一次"
        SECOND = "second", "二次"
        FINAL = "final", "最終"
        OTHER = "other", "その他"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="interviews")
    scheduled_at = models.DateTimeField()
    stage = models.CharField(max_length=20, choices=Stage.choices, default=Stage.FIRST)
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    overall_reflection = models.TextField(blank=True)
    next_action = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.company.name} {self.scheduled_at:%Y-%m-%d}"


class ReflectionItem(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="reflection_items")
    question = models.TextField()
    answer = models.TextField()
    improvement = models.TextField()
    self_score = models.PositiveSmallIntegerField(null=True, blank=True)
    tags = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.question[:30]


class ExamEvent(models.Model):
    class EventType(models.TextChoices):
        MOCK = "mock", "模試"
        DEADLINE = "deadline", "出願締切"
        EXAM = "exam", "入試"
        INTERVIEW = "interview", "面談"
        RESULT = "result", "合格発表"
        OTHER = "other", "その他"

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="exam_events")
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.EXAM)
    scheduled_at = models.DateTimeField("日時")
    location = models.CharField("場所", max_length=200, blank=True)
    memo = models.TextField("メモ", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.school.name} - {self.title}"
    
class StudyLog(models.Model):
    class Subject(models.TextChoices):
        JAPANESE = "japanese", "国語"
        MATH = "math", "数学"
        ENGLISH = "english", "英語"
        SCIENCE = "science", "理科"
        SOCIAL = "social", "社会"
        ESSAY = "essay", "小論文"
        INTERVIEW = "interview", "面接対策"
        OTHER = "other", "その他"

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="study_logs",
        null=True,
        blank=True,
    )
    subject = models.CharField("科目", max_length=20, choices=Subject.choices)
    title = models.CharField("タイトル", max_length=200)
    study_date = models.DateField("学習日")
    duration_minutes = models.PositiveIntegerField("勉強時間（分）", default=60)
    material = models.CharField("教材", max_length=200, blank=True)
    content = models.TextField("学習内容", blank=True)
    next_action = models.TextField("次にやること", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.study_date} {self.get_subject_display()} {self.title}"