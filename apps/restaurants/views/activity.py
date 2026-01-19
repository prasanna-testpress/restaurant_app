from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.restaurants.models import Restaurant

class MyActivityView(LoginRequiredMixin, TemplateView):
    template_name = "restaurants/my_activity.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self._get_user_activity(user=self.request.user)
        )
        return context

    def _get_user_activity(self, user):
        """
        Returns bookmarked and visited restaurants for a user.
        """

        bookmarked = (
            Restaurant.objects
            .filter(bookmarked_by__user=user)
            .distinct()
        )

        visited = (
            Restaurant.objects
            .filter(visited_by__user=user)
            .distinct()
        )

        return {
            "bookmarked_restaurants": bookmarked,
            "visited_restaurants": visited,
        }