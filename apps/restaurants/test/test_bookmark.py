from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.accounts.models import Bookmark
from apps.restaurants.models import Restaurant

User = get_user_model()

class BookmarkToggleViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            city="Chennai",
            address="Addr",
            cost_for_two=300,
            veg_type="veg",
            is_open=True,
        )
        self.url = reverse(
            "restaurants:bookmark",
            kwargs={"restaurant_id": self.restaurant.id},
        )

    def test_bookmark_toggle_requires_login(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"error": "Authentication required"},
        )

    def test_bookmark_toggle_adds_bookmark(self):
        self.client.login(
            email="user@test.com",
            password="password123",
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_bookmarked"])
        self.assertTrue(
            Bookmark.objects.filter(
                user=self.user,
                restaurant=self.restaurant,
            ).exists()
        )

    def test_bookmark_toggle_removes_bookmark(self):
        self.client.login(
            email="user@test.com",
            password="password123",
        )

        # Add
        self.client.post(self.url)

        # Remove
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["is_bookmarked"])
        self.assertFalse(
            Bookmark.objects.filter(
                user=self.user,
                restaurant=self.restaurant,
            ).exists()
        )
