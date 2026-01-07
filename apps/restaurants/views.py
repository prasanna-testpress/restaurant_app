from django.views.generic import ListView

from .models import Restaurant
from .selectors import get_restaurant_list


class RestaurantListView(ListView):
    model = Restaurant
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

    @staticmethod
    def _parse_boolean(value):
        if value == "true":
            return True
        if value == "false":
            return False
        return None
