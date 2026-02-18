from django.conf import settings
from django.db import models

class Company(models.Model):
    class Status(models.TextChoices):
        NOT_APPLIED = "not_applied", "未応募"
        DOCUMENT = "document", "書類選考"
        TEST = "test", "Webテスト"
        FIRST = "first", "一次面接"
        SECOND = "second", "二次面接"
        FINAL = "final", "最終面接"
        OFFER = "offer", "内定"
        CLOSED = "closed", "見送り"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NOT_APPLIED)
    priority = models.PositiveSmallIntegerField(default=3)
    url = models.URLField(blank=True)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
