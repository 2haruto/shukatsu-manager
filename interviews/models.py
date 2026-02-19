from django.db import models
from companies.models import Company


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
    location = models.CharField(max_length=200, blank=True)  # オンライン/対面/URLなど
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
