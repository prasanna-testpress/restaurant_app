from apps.accounts.models import Visited,Bookmark
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant,Cuisine
from apps.restaurants.filters import RestaurantFilter
from apps.reviews.models import Review

User = get_user_model()

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

    def test_filter_by_min_rating(self):
        user1 = User.objects.create_user(
            email="test@example.com",
            password="password",
        )

        user2 = User.objects.create_user(
            email="tewwst@example.com",
            password="password",
        )

        low_rated = Restaurant.objects.create(
            name="Low Rated",
            city="Chennai",
            address="Addr",
            cost_for_two=200,
            veg_type="veg",
        )

        high_rated = Restaurant.objects.create(
            name="High Rated",
            city="Chennai",
            address="Addr",
            cost_for_two=300,
            veg_type="veg",
        )

        no_reviews = Restaurant.objects.create(
            name="No Reviews",
            city="Chennai",
            address="Addr",
            cost_for_two=250,
            veg_type="veg",
        )

       
        Review.objects.create(
            restaurant=low_rated,
            user=user1,
            rating=2,
            comment="Not great",
        )

        Review.objects.create(
            restaurant=high_rated,
            user=user2,
            rating=4,
            comment="Good",
        )
        Review.objects.create(
            restaurant=high_rated,
            user=user1,
            rating=5,
            comment="Excellent",
        )

        queryset = Restaurant.objects.all()

        filterset = RestaurantFilter(
            data={"min_rating": 4},
            queryset=queryset,
        )

        results = filterset.qs

        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first(), high_rated)
        self.assertNotIn(no_reviews, results)


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

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="password",
        )

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

    def test_list_shows_bookmarked_and_visited_flags(self):
        self.client.login(email="user@test.com", password="password")

        restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            city="Chennai",
            address="Test address",
            cost_for_two=300,
            veg_type="veg",
        )
        Bookmark.objects.create(user=self.user, restaurant=restaurant)
        Visited.objects.create(user=self.user, restaurant=restaurant)

        response = self.client.get(reverse("restaurants:restaurant_list"))

        self.assertContains(response, "fa-bookmark")
        self.assertContains(response, "Visited")


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
