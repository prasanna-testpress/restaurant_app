from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(TestCase):

    def test_signup(self):
        response = self.client.post(
            reverse("signup"),
            {
                "email": "user@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="user@example.com").exists())

    def test_login(self):
        User.objects.create_user(
            email="login@example.com",
            password="StrongPass123!",
        )
        response = self.client.post(
            reverse("login"),
            {
                "email": "login@example.com",  # Changed from "username"
                "password": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)  # Changed from 200
