from django.views.generic import ListView

from .models import Restaurant, Cuisine
from .selectors import get_restaurant_list


class RestaurantListView(ListView):
    template_name = "restaurants/list.html"
    context_object_name = "restaurants"
    paginate_by = 10

    def get_queryset(self):
        params = self.request.GET

        return get_restaurant_list(
            city=params.get("city"),
            veg_type=params.get("veg_type"),
            cuisine=params.get("cuisine"),
            sort=params.get("sort"),
            is_open=self._parse_boolean(params.get("is_open")),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["cities"] = (
            Restaurant.objects
            .values_list("city", flat=True)
            .distinct()
            .order_by("city")
        )

        context["cuisines"] = (
            Cuisine.objects
            .values_list("name", flat=True)
            .distinct()
            .order_by("name")
        )

        # Preserve filters during pagination
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params

        return context

    @staticmethod
    def _parse_boolean(value):
        if value == "true":
            return True
        if value == "false":
            return False
        return None
