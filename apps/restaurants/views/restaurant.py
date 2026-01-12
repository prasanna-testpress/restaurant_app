from django.views.generic import ListView, DetailView

from apps.restaurants.filters import RestaurantFilter
from apps.restaurants.models import Restaurant
from apps.restaurants.selectors import (
    get_restaurant_filter_queryset,
    get_spotlight_restaurants,
    get_city_list,
    get_cuisine_list,
    get_restaurant_detail,
    get_restaurant_detail_context,
)


class RestaurantListView(ListView):
    template_name = "restaurants/list.html"
    context_object_name = "restaurants"
    paginate_by = 10

    def get_queryset(self):
        base_qs = get_restaurant_filter_queryset()
        self.filterset = RestaurantFilter(
            data=self.request.GET,
            queryset=base_qs,
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base_qs = self.filterset.qs

        context.update({
            "filter": self.filterset,
            "spotlight_restaurants": get_spotlight_restaurants(base_qs),
            "cities": get_city_list(),
            "cuisines": get_cuisine_list(),
        })

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params

        return context


class RestaurantDetailView(DetailView):
    template_name = "restaurants/detail.html"
    context_object_name = "restaurant"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        return get_restaurant_detail(
            restaurant_id=self.kwargs["id"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            get_restaurant_detail_context(
                restaurant=self.object,
                user=self.request.user,
            )
        )
        return context
