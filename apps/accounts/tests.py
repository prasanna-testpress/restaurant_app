from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

TEST_PASSWORD = "test-password"


class AuthenticationTests(TestCase):

    def test_signup(self):
        response = self.client.post(
            reverse("signup"),
            {
                "email": "user@example.com",
                "password1": TEST_PASSWORD,
                "password2": TEST_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="user@example.com").exists())

    def test_login(self):
        User.objects.create_user(
            email="login@example.com",
            password=TEST_PASSWORD,
        )
        response = self.client.post(
            reverse("login"),
            {
                "email": "login@example.com",
                "password": TEST_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_login_with_wrong_password(self):
        User.objects.create_user(
            email="wrong@example.com",
            password=TEST_PASSWORD,
        )
        response = self.client.post(
            reverse("login"),
            {
                "email": "wrong@example.com",
                "password": "invalid-password",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password")

    def test_signup_password_mismatch(self):
        response = self.client.post(
            reverse("signup"),
            {
                "email": "mismatch@example.com",
                "password1": TEST_PASSWORD,
                "password2": "different-password",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match")
