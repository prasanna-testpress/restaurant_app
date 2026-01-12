from django.db import transaction

from apps.accounts.models import Bookmark
from apps.restaurants.models import Restaurant


class BookmarkService:
    @staticmethod
    @transaction.atomic
    def add(*, user, restaurant_id: int) -> None:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        Bookmark.objects.get_or_create(
            user=user,
            restaurant=restaurant,
        )

    @staticmethod
    @transaction.atomic
    def remove(*, user, restaurant_id: int) -> None:
        Bookmark.objects.filter(
            user=user,
            restaurant_id=restaurant_id,
        ).delete()

    @staticmethod
    def is_bookmarked(*, user, restaurant_id: int) -> bool:
        return Bookmark.objects.filter(
            user=user,
            restaurant_id=restaurant_id,
        ).exists()
