from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.restaurants.models import Restaurant
from apps.accounts.models import Visited

User = get_user_model()


class VisitedViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="pass1234",
        )
        self.restaurant = Restaurant.objects.create(
            name="Visited Restaurant",
            city="Bangalore",
            address="Addr",
            cost_for_two=400,
            veg_type="veg",
        )
        self.url = reverse(
            "restaurants:visited",
            kwargs={"restaurant_id": self.restaurant.id},
        )

    def test_login_required(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_user_can_mark_restaurant_as_visited(self):
        self.client.login(email="user@test.com", password="pass1234")

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Visited.objects.filter(
                user=self.user,
                restaurant=self.restaurant,
            ).exists()
        )

    def test_user_can_unmark_visited_restaurant(self):
        Visited.objects.create(
            user=self.user,
            restaurant=self.restaurant,
        )
        self.client.login(email="user@test.com", password="pass1234")

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Visited.objects.filter(
                user=self.user,
                restaurant=self.restaurant,
            ).exists()
        )
