from django.db.models import Q

from .models import Restaurant


def get_restaurant_list(
    *,
    city=None,
    veg_type=None,
    cuisine=None,
    sort=None,
    is_open=None,
):
    queryset = (
        Restaurant.objects.prefetch_related("images", "cuisines")

    )

    if city:
        queryset = queryset.filter(city__iexact=city)

    if veg_type:
        queryset = queryset.filter(veg_type=veg_type)

    if cuisine:
        queryset = queryset.filter(cuisines__name__iexact=cuisine)

    if is_open is not None:
        queryset = queryset.filter(is_open=is_open)

    if sort == "cost_low":
        queryset = queryset.order_by("cost_for_two")
    elif sort == "cost_high":
        queryset = queryset.order_by("-cost_for_two")
    elif sort == "rating":
        queryset = queryset.order_by("-is_spotlight", "name")  
    else:
        queryset = queryset.order_by("-is_spotlight", "name")

    return queryset.distinct()
