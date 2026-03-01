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
    
    resume_memo = models.TextField("コピペ用メモ", blank=True)
    self_pr = models.TextField("自己PR", blank=True)
    motivation = models.TextField("志望動機", blank=True)
    
    entry_deadline = models.DateField("ES提出締切", blank=True, null=True)
    es_submitted = models.BooleanField("ES提出済み", default=False)
    es_submitted_at = models.DateField("ES提出日", blank=True, null=True)
    es_version_note = models.TextField("提出バージョンメモ", blank=True)
    questions_asked = models.TextField("面接で聞かれたこと", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    

    def __str__(self) -> str:
        return self.name

class School(models.Model):
    class Category(models.TextChoices):
        JUNIOR = "junior", "中学受験"
        HIGH = "high", "高校受験"
        UNIVERSITY = "university", "大学受験"

    class SchoolType(models.TextChoices):
        NATIONAL = "national", "国立"
        PUBLIC = "public", "公立"
        PRIVATE = "private", "私立"

    class Status(models.TextChoices):
        INTERESTED = "interested", "志望中"
        PLAN_TO_APPLY = "plan_to_apply", "出願予定"
        APPLIED = "applied", "出願済"
        EXAM_DONE = "exam_done", "受験済"
        PASSED = "passed", "合格"
        FAILED = "failed", "不合格"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices)
    school_type = models.CharField(max_length=20, choices=SchoolType.choices, blank=True)
    deviation_value = models.PositiveSmallIntegerField("偏差値", null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INTERESTED)
    exam_date = models.DateField("受験日", null=True, blank=True)
    url = models.URLField(blank=True)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
