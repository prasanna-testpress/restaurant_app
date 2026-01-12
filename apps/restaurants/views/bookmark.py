from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.restaurants.services.bookmark_service import BookmarkService


class BookmarkView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id, *args, **kwargs):
        BookmarkService.add(
            user=request.user,
            restaurant_id=restaurant_id,
        )
        return JsonResponse({"bookmarked": True}, status=200)

    def delete(self, request, restaurant_id, *args, **kwargs):
        BookmarkService.remove(
            user=request.user,
            restaurant_id=restaurant_id,
        )
        return JsonResponse({"bookmarked": False}, status=200)
