from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Company, School

User = get_user_model()


class CompanySecurityTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass12345")
        self.user2 = User.objects.create_user(username="user2", password="pass12345")

        self.company1 = Company.objects.create(
            owner=self.user1,
            name="Sony",
            role="エンジニア",
        )
        self.company2 = Company.objects.create(
            owner=self.user2,
            name="Nintendo",
            role="プログラマ",
        )

    def test_company_list_shows_only_my_companies(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("company_list"))

        self.assertContains(response, "Sony")
        self.assertNotContains(response, "Nintendo")

    def test_cannot_view_other_users_company_detail(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("company_detail", args=[self.company2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_cannot_edit_other_users_company(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("company_update", args=[self.company2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_cannot_delete_other_users_company(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.post(reverse("company_delete", args=[self.company2.pk]))
        self.assertEqual(response.status_code, 404)


class SchoolSecurityTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass12345")
        self.user2 = User.objects.create_user(username="user2", password="pass12345")

        self.school1 = School.objects.create(
            owner=self.user1,
            name="第一志望高校",
            category="high",
        )
        self.school2 = School.objects.create(
            owner=self.user2,
            name="別ユーザーの学校",
            category="high",
        )

    def test_school_list_shows_only_my_schools(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("school_list"))

        self.assertContains(response, "第一志望高校")
        self.assertNotContains(response, "別ユーザーの学校")

    def test_cannot_view_other_users_school_detail(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("school_detail", args=[self.school2.pk]))
        self.assertEqual(response.status_code, 404)