# apps/restaurants/views/visited.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.restaurants.domain import toggle_visited
from apps.restaurants.exceptions import RestaurantNotFound


class VisitedToggleView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        return JsonResponse(
            {"error": "Authentication required"},
            status=401,
        )

    def post(self, request, restaurant_id, *args, **kwargs):
        try:
            is_visited = toggle_visited(
                user=request.user,
                restaurant_id=restaurant_id,
            )
        except RestaurantNotFound:
            return JsonResponse(
                {"error": "Restaurant not found"},
                status=404,
            )

        return JsonResponse(
            {
                "is_visited": is_visited,
                "message": (
                    "Marked as visited"
                    if is_visited
                    else "Marked as not visited"
                ),
            },
            status=200,
        )
