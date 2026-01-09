from django.contrib import admin

from apps.restaurants.models import (
    Cuisine,
    Restaurant,
    MenuItem,
    RestaurantImage,
)


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "city",
        "veg_type",
        "cost_for_two",
        "is_open",
        "is_spotlight",
    ]
    list_filter = ["city", "veg_type", "is_open", "is_spotlight"]
    search_fields = ["name", "city"]
    filter_horizontal = ["cuisines"]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["name", "restaurant", "price"]
    list_filter = ["restaurant"]
    search_fields = ["name", "restaurant__name"]


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ["restaurant", "uploaded_at"]
    list_filter = ["restaurant"]
