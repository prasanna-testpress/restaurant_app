from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

TEST_PASSWORD = "test-password-not-secret"


class SignupTests(TestCase):
    """
    Tests related to user signup.
    """

    def test_signup_creates_user(self):
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

    def test_signup_logs_user_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "email": "loggedin@example.com",
                "password1": TEST_PASSWORD,
                "password2": TEST_PASSWORD,
            },
            follow=True,
        )

        user = User.objects.get(email="loggedin@example.com")
        request_user = response.wsgi_request.user

        self.assertTrue(request_user.is_authenticated)
        self.assertEqual(request_user, user)

    def test_signup_password_mismatch_shows_error(self):
        response = self.client.post(
            reverse("signup"),
            {
                "email": "mismatch@example.com",
                "password1": TEST_PASSWORD,
                "password2": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match")


class LoginTests(TestCase):
    """
    Tests related to user login.
    """

    def test_login_success_redirects(self):
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

    def test_login_logs_user_in(self):
        user = User.objects.create_user(
            email="loggedin2@example.com",
            password=TEST_PASSWORD,
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "loggedin2@example.com",
                "password": TEST_PASSWORD,
            },
            follow=True,
        )

        request_user = response.wsgi_request.user

        self.assertTrue(request_user.is_authenticated)
        self.assertEqual(request_user, user)

    def test_login_with_wrong_password_shows_error(self):
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

    def test_login_with_nonexistent_email_shows_error(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": "nosuchuser@example.com",
                "password": TEST_PASSWORD,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password")

    def test_inactive_user_cannot_login(self):
        User.objects.create_user(
            email="inactive@example.com",
            password=TEST_PASSWORD,
            is_active=False,
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "inactive@example.com",
                "password": TEST_PASSWORD,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password")


class AccessControlTests(TestCase):
    """
    Tests related to access control and redirects.
    """

    def test_authenticated_user_redirected_from_login_page(self):
        user = User.objects.create_user(
            email="already@example.com",
            password=TEST_PASSWORD,
        )
        self.client.login(email="already@example.com", password=TEST_PASSWORD)

        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 302)


class LogoutTests(TestCase):
    """
    Tests related to user logout.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email="logout@example.com",
            password=TEST_PASSWORD,
        )

    def test_logout_logs_user_out(self):
        self.client.login(email="logout@example.com", password=TEST_PASSWORD)

        response = self.client.post(
            reverse("logout"),
            follow=True,
        )

        request_user = response.wsgi_request.user
        self.assertFalse(request_user.is_authenticated)

    def test_logout_redirects(self):
        self.client.login(email="logout@example.com", password=TEST_PASSWORD)

        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, 302)

    def test_logout_when_not_authenticated_is_safe(self):
        response = self.client.post(
            reverse("logout"),
            follow=True,
        )

        request_user = response.wsgi_request.user
        self.assertFalse(request_user.is_authenticated)

    def test_get_logout_is_not_allowed(self):
        self.client.login(email="logout@example.com", password=TEST_PASSWORD)

        response = self.client.get(reverse("logout"))

        # Accept redirect or method-not-allowed (both valid)
        self.assertIn(response.status_code, (302, 405))
