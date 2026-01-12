from django.urls import reverse
from django.test import TestCase

from apps.restaurants.models import Restaurant,Cuisine
from apps.restaurants.filters import RestaurantFilter

class RestaurantFilterTests(TestCase):

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

        queryset = Restaurant.objects.all()
        filterset = RestaurantFilter(
            data={"city": "chennai"},
            queryset=queryset,
        )

        results = filterset.qs

        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().city, "Chennai")

    def test_spotlight_restaurants_appear_first_by_default(self):
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

        filterset = RestaurantFilter(
            data={},
            queryset=Restaurant.objects.all(),
        )

        restaurants = list(filterset.qs)

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

        response = self.client.get(reverse("restaurants:restaurant_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Restaurant")

class RestaurantDetailTests(TestCase):

    def setUp(self):
        self.cuisine = Cuisine.objects.create(name="Indian")
        self.restaurant = Restaurant.objects.create(
            name="Spice Hub",
            city="Chennai",
            address="Main Road",
            cost_for_two=500,
        )
        self.restaurant.cuisines.add(self.cuisine)

    def test_detail_page_loads(self):
        url = reverse("restaurants:restaurant_detail", args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spice Hub")

    def test_detail_page_404(self):
        url = reverse("restaurants:restaurant_detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)