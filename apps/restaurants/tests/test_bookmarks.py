from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.restaurants.models import Restaurant
from apps.accounts.models import Bookmark

User = get_user_model()


class BookmarkViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="pass1234",
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            city="Chennai",
            address="Addr",
            cost_for_two=300,
            veg_type="veg",
        )
        self.url = reverse(
            "restaurants:bookmark",
            kwargs={"restaurant_id": self.restaurant.id},
        )

    def test_login_required(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_user_can_bookmark_restaurant(self):
        self.client.login(email="user@test.com", password="pass1234")

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Bookmark.objects.filter(
                user=self.user,
                restaurant=self.restaurant,
            ).exists()
        )

    def test_user_can_unbookmark_restaurant(self):
        Bookmark.objects.create(
            user=self.user,
            restaurant=self.restaurant,
        )
        self.client.login(email="user@test.com", password="pass1234")

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Bookmark.objects.filter(
                user=self.user,
                restaurant=self.restaurant,
            ).exists()
        )
