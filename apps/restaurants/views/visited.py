from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.accounts.models import Visited
from apps.restaurants.models import Restaurant
from apps.restaurants.domain import is_restaurant_visited

User = get_user_model()

class RestaurantNotFound(Exception):
    pass


class VisitedToggleView(LoginRequiredMixin, View):

    def handle_no_permission(self):
        return JsonResponse(
            {"error": "Authentication required"},
            status=401,
        )

    def post(self, request, restaurant_id, *args, **kwargs):
        try:
            was_visited = is_restaurant_visited(
                user=request.user,
                restaurant_id=restaurant_id,
            )

            if was_visited:
                self._unmark_visited(
                    user=request.user,
                    restaurant_id=restaurant_id,
                )
                message = "Marked as not visited"
            else:
                self._mark_visited(
                    user=request.user,
                    restaurant_id=restaurant_id,
                )
                message = "Marked as visited"

            return JsonResponse(
                {
                    "message": message,
                    "is_visited": not was_visited,
                },
                status=200,
            )

        except RestaurantNotFound:
            return JsonResponse(
                {"error": "Restaurant not found"},
                status=404,
            )
    
    
    def _mark_visited(self, user: User, restaurant_id: int) -> None:
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise RestaurantNotFound("Restaurant does not exist")

        Visited.objects.get_or_create(
            user=user,
            restaurant=restaurant,
        )


    def _unmark_visited(self, user: User, restaurant_id: int) -> None:
        Visited.objects.filter(
            user=user,
            restaurant_id=restaurant_id,
        ).delete()
