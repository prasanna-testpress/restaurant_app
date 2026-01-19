from apps.restaurants.exceptions import RestaurantNotFound
from apps.accounts.models import Bookmark, Visited
from apps.restaurants.models import Restaurant
from django.db import transaction
from apps.reviews.models import Review
from typing import Optional



def is_restaurant_bookmarked(*, user, restaurant_id: int) -> bool:
    return Bookmark.objects.filter(
        user=user,
        restaurant_id=restaurant_id,
    ).exists()

def is_restaurant_visited(*, user, restaurant_id: int) -> bool:
    return Visited.objects.filter(
        user=user,
        restaurant_id=restaurant_id,
    ).exists()


@transaction.atomic
def toggle_visited(*, user, restaurant_id: int) -> bool:
    """
    Toggles visited state.
    Returns True if visited after toggle, False otherwise.
    """
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        raise RestaurantNotFound

    visited, created = Visited.objects.get_or_create(
        user=user,
        restaurant=restaurant,
    )

    if not created:
        visited.delete()
        return False

    return True

def get_user_review_for_restaurant(*, user: User, restaurant: Restaurant) -> Optional[Review]:
    return Review.objects.filter(user=user, restaurant=restaurant).first()

