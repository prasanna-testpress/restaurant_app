from typing import Optional

from django.db.models import Case, IntegerField, Value, When

from .models import Restaurant


def get_restaurant_list(
    *,
    city: Optional[str] = None,
    veg_type: Optional[str] = None,
    is_open: Optional[bool] = None,
    cuisine: Optional[str] = None,
    sort: Optional[str] = None,
):
    queryset = Restaurant.objects.all()

    if city:
        queryset = queryset.filter(city__iexact=city)

    if veg_type:
        queryset = queryset.filter(veg_type=veg_type)

    if is_open is not None:
        queryset = queryset.filter(is_open=is_open)

    if cuisine:
        queryset = queryset.filter(cuisines__name__iexact=cuisine)

    queryset = queryset.distinct()

    # Spotlight restaurants first
    queryset = queryset.annotate(
        spotlight_order=Case(
            When(is_spotlight=True, then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        )
    )

    if sort == "cost":
        queryset = queryset.order_by("spotlight_order", "cost_for_two")

    else:
        queryset = queryset.order_by("spotlight_order", "name")

    return queryset
