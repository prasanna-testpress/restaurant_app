from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.restaurants.services.visited_service import VisitedService


class VisitedView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id, *args, **kwargs):
        VisitedService.add(
            user=request.user,
            restaurant_id=restaurant_id,
        )
        return JsonResponse({"visited": True}, status=200)

    def delete(self, request, restaurant_id, *args, **kwargs):
        VisitedService.remove(
            user=request.user,
            restaurant_id=restaurant_id,
        )
        return JsonResponse({"visited": False}, status=200)
