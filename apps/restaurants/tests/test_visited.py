from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User, Visited
from apps.restaurants.models import Cuisine, Restaurant


class VisitedViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
        )

        self.restaurant = self._create_restaurant()

        self.client.login(
            email="user@test.com",
            password="password123",
        )

    def _create_restaurant(self):
        restaurant = Restaurant.objects.create(
            name="Visited Restaurant",
            city="Bangalore",
            address="123 Test Street",
            cost_for_two=500,
            veg_type=Restaurant.VegChoices.VEG,
            is_open=True,
        )

        cuisine = Cuisine.objects.create(name="Indian")
        restaurant.cuisines.add(cuisine)

        return restaurant

    def test_user_can_mark_restaurant_as_visited(self):
        url = reverse(
            "restaurants:restaurant-visited",
            kwargs={"restaurant_id": self.restaurant.id},
        )

        response = self.client.post(url)

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

        url = reverse(
            "restaurants:restaurant-visited",
            kwargs={"restaurant_id": self.restaurant.id},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Visited.objects.filter(
                user=self.user,
                restaurant=self.restaurant,
            ).exists()
        )
