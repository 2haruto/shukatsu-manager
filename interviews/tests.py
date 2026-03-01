from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from companies.models import Company, School
from .models import Interview, ExamEvent, StudyLog

User = get_user_model()


class InterviewSecurityTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass12345")
        self.user2 = User.objects.create_user(username="user2", password="pass12345")

        self.company1 = Company.objects.create(owner=self.user1, name="Sony")
        self.company2 = Company.objects.create(owner=self.user2, name="Nintendo")

        self.interview1 = Interview.objects.create(
            company=self.company1,
            scheduled_at=timezone.now(),
            stage="first",
        )
        self.interview2 = Interview.objects.create(
            company=self.company2,
            scheduled_at=timezone.now(),
            stage="first",
        )

    def test_interview_list_shows_only_my_interviews(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("interview_list"))

        self.assertContains(response, "Sony")
        self.assertNotContains(response, "Nintendo")

    def test_cannot_view_other_users_interview_detail(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("interview_detail", args=[self.interview2.pk]))
        self.assertEqual(response.status_code, 404)


class StudentModeSecurityTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass12345")
        self.user2 = User.objects.create_user(username="user2", password="pass12345")

        self.school1 = School.objects.create(owner=self.user1, name="自分の学校", category="high")
        self.school2 = School.objects.create(owner=self.user2, name="他人の学校", category="high")

        self.event1 = ExamEvent.objects.create(
            school=self.school1,
            title="自分の模試",
            event_type="mock",
            scheduled_at=timezone.now(),
        )
        self.event2 = ExamEvent.objects.create(
            school=self.school2,
            title="他人の模試",
            event_type="mock",
            scheduled_at=timezone.now(),
        )

        self.log1 = StudyLog.objects.create(
            school=self.school1,
            subject="math",
            title="数学演習",
            study_date=timezone.localdate(),
            duration_minutes=60,
        )
        self.log2 = StudyLog.objects.create(
            school=self.school2,
            subject="english",
            title="英語長文",
            study_date=timezone.localdate(),
            duration_minutes=60,
        )

    def test_exam_event_list_shows_only_my_events(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("exam_event_list"))

        self.assertContains(response, "自分の模試")
        self.assertNotContains(response, "他人の模試")

    def test_study_log_list_shows_only_my_logs(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("study_log_list"))

        self.assertContains(response, "数学演習")
        self.assertNotContains(response, "英語長文")

    def test_cannot_view_other_users_exam_event_detail(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("exam_event_detail", args=[self.event2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_cannot_view_other_users_study_log_detail(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("study_log_detail", args=[self.log2.pk]))
        self.assertEqual(response.status_code, 404)