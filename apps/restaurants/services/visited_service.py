from django.db import transaction

from apps.accounts.models import Visited
from apps.restaurants.models import Restaurant


class VisitedService:
    @staticmethod
    @transaction.atomic
    def add(*, user, restaurant_id: int) -> None:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        Visited.objects.get_or_create(
            user=user,
            restaurant=restaurant,
        )

    @staticmethod
    @transaction.atomic
    def remove(*, user, restaurant_id: int) -> None:
        Visited.objects.filter(
            user=user,
            restaurant_id=restaurant_id,
        ).delete()

    @staticmethod
    def is_visited(*, user, restaurant_id: int) -> bool:
        return Visited.objects.filter(
            user=user,
            restaurant_id=restaurant_id,
        ).exists()
