from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.restaurants.models import Restaurant
from apps.accounts.models import Bookmark, Visited

User = get_user_model()


class ActivityBaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123"
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="password123"
        )

        self.restaurant1 = Restaurant.objects.create(
            name="Restaurant 1",
            city="Chennai",
            cost_for_two=500
        )

        self.restaurant2 = Restaurant.objects.create(
            name="Restaurant 2",
            city="Bangalore",
            cost_for_two=700
        )

        self.client.login(email="test@example.com", password="password123")


class MyActivityViewTests(ActivityBaseTestCase):

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse("restaurants:my_activity"))
        self.assertEqual(response.status_code, 302)

    def test_activity_page_renders(self):
        response = self.client.get(reverse("restaurants:my_activity"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/my_activity.html")


class MyBookmarksViewTests(ActivityBaseTestCase):

    def setUp(self):
        super().setUp()

        Bookmark.objects.create(
            user=self.user,
            restaurant=self.restaurant1
        )

        Bookmark.objects.create(
            user=self.other_user,
            restaurant=self.restaurant2
        )

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse("restaurants:my_bookmarks"))
        self.assertEqual(response.status_code, 302)

    def test_only_user_bookmarks_are_returned(self):
        response = self.client.get(reverse("restaurants:my_bookmarks"))
        self.assertEqual(response.status_code, 200)

        page_obj = response.context["page_obj"]
        self.assertEqual(len(page_obj), 1)
        self.assertEqual(page_obj[0], self.restaurant1)

    def test_empty_state_context(self):
        Bookmark.objects.all().delete()

        response = self.client.get(reverse("restaurants:my_bookmarks"))

        self.assertContains(response, "No Bookmarks Yet")
        self.assertContains(response, "Save restaurants you want to visit later.")

    def test_pagination(self):
        for i in range(10):
            restaurant = Restaurant.objects.create(
                name=f"Restaurant {i}",
                cost_for_two=400,
                city=f"City {i}",
            )
            Bookmark.objects.create(
                user=self.user,
                restaurant=restaurant
            )

        response = self.client.get(reverse("restaurants:my_bookmarks"))
        self.assertEqual(len(response.context["page_obj"]), 1)


class MyVisitedViewTests(ActivityBaseTestCase):

    def setUp(self):
        super().setUp()

        Visited.objects.create(
            user=self.user,
            restaurant=self.restaurant1
        )

    def test_visited_restaurants_returned(self):
        response = self.client.get(reverse("restaurants:my_visited"))
        self.assertEqual(response.status_code, 200)

        page_obj = response.context["page_obj"]
        self.assertEqual(len(page_obj), 1)
        self.assertEqual(page_obj[0], self.restaurant1)

    def test_empty_state(self):
        Visited.objects.all().delete()

        response = self.client.get(reverse("restaurants:my_visited"))

        self.assertContains(response, "No Visited Places")
        self.assertContains(
            response,
            "Mark restaurants as visited to track your culinary journey."
        )
