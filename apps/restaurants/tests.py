from django.urls import reverse
from django.test import TestCase

from apps.restaurants.models import Restaurant
from apps.restaurants.selectors import get_restaurant_list


class RestaurantSelectorTests(TestCase):

    def test_filter_by_city(self):
        Restaurant.objects.create(
            name="Chennai Veg",
            city="Chennai",
            address="Addr",
            cost_for_two=200,
            veg_type="veg",
        )
        Restaurant.objects.create(
            name="Bangalore Veg",
            city="Bangalore",
            address="Addr",
            cost_for_two=200,
            veg_type="veg",
        )

        restaurants = get_restaurant_list(city="chennai")

        self.assertEqual(restaurants.count(), 1)
        self.assertEqual(restaurants.first().city, "Chennai")

    def test_spotlight_restaurants_appear_first(self):
        Restaurant.objects.create(
            name="Normal",
            city="Chennai",
            address="Addr",
            cost_for_two=300,
            veg_type="veg",
            is_spotlight=False,
        )
        spotlight = Restaurant.objects.create(
            name="Spotlight",
            city="Chennai",
            address="Addr",
            cost_for_two=300,
            veg_type="veg",
            is_spotlight=True,
        )

        restaurants = list(get_restaurant_list())

        self.assertEqual(restaurants[0], spotlight)

class RestaurantListViewTests(TestCase):

    def test_restaurant_list_page_loads(self):
        Restaurant.objects.create(
            name="Test Restaurant",
            city="Chennai",
            address="Addr",
            cost_for_two=250,
            veg_type="veg",
        )

        response = self.client.get(reverse("restaurant_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Restaurant")