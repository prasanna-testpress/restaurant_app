
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.accounts.models import Bookmark
from apps.restaurants.models import Restaurant
from django.contrib.auth import get_user_model
from apps.restaurants.domain import is_restaurant_bookmarked

User = get_user_model()

class RestaurantNotFound(Exception):
    pass


class BookmarkToggleView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        return JsonResponse(
            {"error": "Authentication required"},
            status=401,
        )

    def post(self, request, restaurant_id, *args, **kwargs):
        try:
            was_bookmarked = is_restaurant_bookmarked(
                user=request.user,
                restaurant_id=restaurant_id,
            )

            if was_bookmarked:
                self._remove_bookmark(
                    user=request.user,
                    restaurant_id=restaurant_id,
                )
                message = "Bookmark removed"
            else:
                self._add_bookmark(
                    user=request.user,
                    restaurant_id=restaurant_id,
                )
                message = "Restaurant bookmarked"

            return JsonResponse(
                {
                    "message": message,
                    "is_bookmarked": not was_bookmarked,
                },
                status=200,
            )

        except RestaurantNotFound:
            return JsonResponse(
                {"error": "Restaurant not found"},
                status=404,
            )

    def _add_bookmark(self, user: User, restaurant_id: int) -> None:
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise RestaurantNotFound("Restaurant does not exist")

        Bookmark.objects.get_or_create(
            user=user,
            restaurant=restaurant,
        )

    def _remove_bookmark(self, user: User, restaurant_id: int) -> None:
        Bookmark.objects.filter(
            user=user,
            restaurant_id=restaurant_id,
        ).delete()

