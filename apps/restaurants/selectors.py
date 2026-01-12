from django.db.models import Avg, Count, Prefetch
from django.shortcuts import get_object_or_404

from apps.restaurants.models import Restaurant, MenuItem, RestaurantImage, Cuisine
from apps.reviews.models import Review


# ---------- LIST SELECTORS ----------

def get_restaurant_filter_queryset():
    return Restaurant.objects.prefetch_related(
        "images",
        "cuisines",
    )


def get_spotlight_restaurants(qs):
    return qs.filter(is_spotlight=True)


def get_city_list():
    return (
        Restaurant.objects
        .values_list("city", flat=True)
        .distinct()
        .order_by("city")
    )


def get_cuisine_list():
    return (
        Cuisine.objects
        .values_list("name", flat=True)
        .distinct()
        .order_by("name")
    )


# ---------- DETAIL SELECTORS ----------

def get_restaurant_detail(*, restaurant_id: int) -> Restaurant:
    return get_object_or_404(
        Restaurant.objects
        .prefetch_related(
            "cuisines",
            Prefetch(
                "menu_items",
                queryset=MenuItem.objects.order_by("name"),
            ),
            Prefetch(
                "images",
                queryset=RestaurantImage.objects.order_by("uploaded_at"),
            ),
            Prefetch(
                "reviews",
                queryset=Review.objects
                .select_related("user")
                .order_by("-created_at"),
            ),
        )
        .annotate(
            avg_rating=Avg("reviews__rating"),
            review_count=Count("reviews"),
        ),
        id=restaurant_id,
    )


def get_restaurant_detail_context(*, restaurant, user=None):
    if not user or not user.is_authenticated:
        return {
            "is_bookmarked": False,
            "is_visited": False,
        }

    return {
        "is_bookmarked": restaurant.bookmarked_by.filter(user=user).exists(),
        "is_visited": restaurant.visited_by.filter(user=user).exists(),
    }
