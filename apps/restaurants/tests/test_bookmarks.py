from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User, Bookmark
from apps.restaurants.models import Restaurant, Cuisine


class BookmarkViewTests(TestCase):
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
            name="Test Restaurant",
            city="Chennai",
            address="123 Food Street",
            cost_for_two=400,
            veg_type=Restaurant.VegChoices.NON_VEG,
            is_open=True,
        )

        cuisine = Cuisine.objects.create(name="South Indian")
        restaurant.cuisines.add(cuisine)

        return restaurant

    def test_user_can_bookmark_restaurant(self):
        url = reverse(
            "restaurants:restaurant-bookmark",
            kwargs={"restaurant_id": self.restaurant.id},
        )

        response = self.client.post(url)

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

        url = reverse(
            "restaurants:restaurant-bookmark",
            kwargs={"restaurant_id": self.restaurant.id},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Bookmark.objects.filter(
                user=self.user,
                restaurant=self.restaurant,
            ).exists()
        )
