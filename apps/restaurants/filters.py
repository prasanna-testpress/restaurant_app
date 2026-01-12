import django_filters

from apps.restaurants.models import Restaurant


class RestaurantFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(
        field_name="city",
        lookup_expr="iexact",
    )
    veg_type = django_filters.CharFilter(
        field_name="veg_type",
    )
    cuisine = django_filters.CharFilter(
        field_name="cuisines__name",
        lookup_expr="iexact",
    )
    is_open = django_filters.BooleanFilter(
        field_name="is_open",
    )

    sort = django_filters.ChoiceFilter(
        method="filter_sort",
        choices=(
            ("cost_low", "Cost: Low to High"),
            ("cost_high", "Cost: High to Low"),
        ),
    )

    class Meta:
        model = Restaurant
        fields = [
            "city",
            "veg_type",
            "cuisine",
            "is_open",
        ]

    def filter_sort(self, queryset, name, value):
        if value == "cost_low":
            return queryset.order_by("cost_for_two")
        if value == "cost_high":
            return queryset.order_by("-cost_for_two")
        return queryset

    @property
    def qs(self):
        queryset = super().qs.distinct()

        # Default ordering: spotlight first
        if not self.data.get("sort"):
            return queryset.order_by("-is_spotlight", "name")

        return queryset
