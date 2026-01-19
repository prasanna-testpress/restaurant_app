from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.paginator import Paginator

from apps.restaurants.models import Restaurant

class MyActivityView(LoginRequiredMixin, TemplateView):
    template_name = "restaurants/my_activity.html"

    BOOKMARKS_PER_PAGE = 9 
    VISITED_PER_PAGE = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity = self._get_user_activity(user=self.request.user)

        context["bookmarks_page"] = self._paginate(
            queryset=activity["bookmarked_restaurants"],
            page_param="bookmarks_page",
            per_page=self.BOOKMARKS_PER_PAGE,
        )

        context["visited_page"] = self._paginate(
            queryset=activity["visited_restaurants"],
            page_param="visited_page",
            per_page=self.VISITED_PER_PAGE,
        )
        
        context["active_tab"] = self.request.GET.get('tab', 'bookmarks')

        return context

    def _get_user_activity(self, *, user):
        base_qs = Restaurant.objects.annotate(rating=Avg('reviews__rating')).prefetch_related('cuisines')

        bookmarked = (
            base_qs
            .filter(bookmarked_by__user=user)
            .distinct()
            .order_by("-created_at")
        )

        visited = (
            base_qs
            .filter(visited_by__user=user)
            .distinct()
            .order_by("-created_at")
        )

        return {
            "bookmarked_restaurants": bookmarked,
            "visited_restaurants": visited,
        }

    def _paginate(self, *, queryset, page_param: str, per_page: int):
        paginator = Paginator(queryset, per_page)
        page_number = self.request.GET.get(page_param)
        return paginator.get_page(page_number)