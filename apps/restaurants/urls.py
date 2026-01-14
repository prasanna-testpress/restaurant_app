from django.urls import path

from apps.restaurants.views import (
    RestaurantListView,
    RestaurantDetailView,
    BookmarkToggleView,
)


app_name = "restaurants"
urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant_list"),
    path("<int:id>/", RestaurantDetailView.as_view(), name="restaurant_detail"),
    path("<int:restaurant_id>/bookmark/", BookmarkToggleView.as_view(), name="bookmark"),
]
