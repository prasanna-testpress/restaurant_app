from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from apps.restaurants.models import Restaurant


class UserRestaurantActivityMixin:
    def get_base_queryset(self):
        return (
            Restaurant.objects
            .annotate(rating=Avg("reviews__rating"))
            .prefetch_related("cuisines")
        )


class MyActivityView(LoginRequiredMixin, TemplateView):
    template_name = "restaurants/my_activity.html"


class MyBookmarksView(LoginRequiredMixin, UserRestaurantActivityMixin, ListView):
    template_name = "restaurants/includes/_activity_list.html"
    paginate_by = 1

    def get_queryset(self):
        return (
            self.get_base_queryset()
            .filter(bookmarked_by__user=self.request.user)
            .distinct()
            .order_by("-bookmarked_by__created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "empty_title": "No Bookmarks Yet",
            "empty_message": "Save restaurants you want to visit later.",
            "empty_icon": "fa-regular fa-bookmark"
        })
        return context


class MyVisitedView(LoginRequiredMixin, UserRestaurantActivityMixin, ListView):
    template_name = "restaurants/includes/_activity_list.html"
    paginate_by = 1

    def get_queryset(self):
        return (
            self.get_base_queryset()
            .filter(visited_by__user=self.request.user)
            .distinct()
            .order_by("-visited_by__visited_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "empty_title": "No Visited Places",
            "empty_message": "Mark restaurants as visited to track your culinary journey.",
            "empty_icon": "fa-solid fa-utensils"
        })
        return context
