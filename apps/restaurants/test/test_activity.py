from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.restaurants.models import Restaurant
from apps.accounts.models import Bookmark, Visited

User = get_user_model()


class MyActivityTests(TestCase):
    def setUp(self):
        self.password = "password123"
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password=self.password,
        )
        self.client.login(email=self.user.email, password=self.password)

        self.restaurants = []
        for i in range(15):
            restaurant = Restaurant.objects.create(
                name=f"Restaurant {i}",
                city="Test City",
                address=f"Address {i}",
                cost_for_two=500,
                veg_type="veg",
            )
            self.restaurants.append(restaurant)

        Bookmark.objects.bulk_create([
            Bookmark(user=self.user, restaurant=self.restaurants[i]) for i in range(10)
        ])

        Visited.objects.bulk_create([
            Visited(user=self.user, restaurant=self.restaurants[i]) for i in range(10, 15)
        ])

        self.url = reverse("restaurants:my_activity")


    def test_my_activity_context_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        bookmarks_page = response.context["bookmarks_page"]
        self.assertEqual(len(bookmarks_page), 9)
        self.assertEqual(bookmarks_page.paginator.count, 10)

        visited_page = response.context["visited_page"]
        self.assertEqual(len(visited_page), 5)
        self.assertEqual(visited_page.paginator.count, 5)

        self.assertEqual(response.context["active_tab"], "bookmarks")

    def test_my_activity_tab_selection(self):
        response = self.client.get(f"{self.url}?tab=visited")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["active_tab"], "visited")

    def test_my_activity_pagination(self):
        response = self.client.get(f"{self.url}?bookmarks_page=2")
        self.assertEqual(response.status_code, 200)
        bookmarks_page = response.context["bookmarks_page"]
        self.assertEqual(len(bookmarks_page), 1)  
