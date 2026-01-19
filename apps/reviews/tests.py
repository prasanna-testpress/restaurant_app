from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.restaurants.models import Restaurant
from apps.reviews.models import Review

User = get_user_model()


class ReviewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
        )

        self.other_user = User.objects.create_user(
            email="other@test.com",
            password="password123",
        )

        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            city="Chennai",
            address="Address",
            cost_for_two=300,
            veg_type="veg",
        )


    def test_authenticated_user_can_create_review(self):
        self.client.login(email="user@test.com", password="password123")

        response = self.client.post(
            reverse("reviews:submit", args=[self.restaurant.id]),
            {
                "rating": 4,
                "comment": "Great food!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)

        review = Review.objects.first()
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Great food!")
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.restaurant, self.restaurant)

    def test_anonymous_user_cannot_create_review(self):
        response = self.client.post(
            reverse("reviews:submit", args=[self.restaurant.id]),
            {
                "rating": 5,
                "comment": "Nice",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)


    def test_user_can_update_own_review(self):
        review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            rating=3,
            comment="Okay",
        )

        self.client.login(email="user@test.com", password="password123")

        response = self.client.post(
            reverse("reviews:submit", args=[self.restaurant.id]),
            {
                "rating": 5,
                "comment": "Excellent!",
            },
        )

        review.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent!")

    def test_user_cannot_create_second_review(self):
        Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            rating=4,
            comment="Good",
        )

        self.client.login(email="user@test.com", password="password123")

        self.client.post(
            reverse("reviews:submit", args=[self.restaurant.id]),
            {
                "rating": 2,
                "comment": "Bad",
            },
        )

        self.assertEqual(Review.objects.count(), 1)


    def test_user_can_delete_own_review(self):
        review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            rating=4,
            comment="Nice",
        )

        self.client.login(email="user@test.com", password="password123")

        response = self.client.post(
            reverse("reviews:delete", args=[review.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)

    def test_user_cannot_delete_other_users_review(self):
        review = Review.objects.create(
            user=self.other_user,
            restaurant=self.restaurant,
            rating=5,
            comment="Amazing",
        )

        self.client.login(email="user@test.com", password="password123")

        response = self.client.post(
            reverse("reviews:delete", args=[review.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Review.objects.count(), 1)



    def test_reviews_visible_on_restaurant_detail_page(self):
        Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            rating=5,
            comment="Loved it",
        )

        response = self.client.get(
            reverse("restaurants:restaurant_detail", args=[self.restaurant.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Loved it")
        self.assertContains(response, "user@test.com")
