from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.accounts.models import Visited
from apps.restaurants.models import Restaurant

User = get_user_model()


class VisitedToggleViewTests(TestCase):

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
            "restaurants:visited",
            kwargs={"restaurant_id": self.restaurant.id},
        )

    def test_visited_requires_login(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)

    def test_visited_toggle_with_invalid_restaurant_id(self):
        self.client.login(
            email="user@test.com",
            password="password123",
        )

        invalid_url = reverse(
            "restaurants:visited",
            kwargs={"restaurant_id": 999},
        )

        response = self.client.post(invalid_url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"error": "Restaurant not found"},
        )


    def test_mark_visited(self):
        self.client.login(
            email="user@test.com",
            password="password123",
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_visited"])
        self.assertTrue(
            Visited.objects.filter(
                user=self.user,
                restaurant=self.restaurant,
            ).exists()
        )

    def test_unmark_visited(self):
        self.client.login(
            email="user@test.com",
            password="password123",
        )

        self.client.post(self.url)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["is_visited"])
        self.assertFalse(
            Visited.objects.filter(
                user=self.user,
                restaurant=self.restaurant,
            ).exists()
        )

