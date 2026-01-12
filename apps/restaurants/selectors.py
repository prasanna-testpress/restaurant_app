from django.db.models import Avg,Count, Prefetch
from django.shortcuts import get_object_or_404

from .models import Restaurant, MenuItem, RestaurantImage
from apps.reviews.models import Review


def get_restaurant_detail(*, restaurant_id: int) -> Restaurant:
    return get_object_or_404(
        Restaurant.objects
        .prefetch_related(
            "cuisines",
            Prefetch("menu_items", queryset=MenuItem.objects.order_by("name")),
            Prefetch("images", queryset=RestaurantImage.objects.order_by("uploaded_at")),
            Prefetch("reviews", queryset=Review.objects.select_related("user").order_by("-created_at")),
        )
        .annotate(avg_rating=Avg("reviews__rating"),review_count=Count("reviews"),),
        id=restaurant_id,
    )
