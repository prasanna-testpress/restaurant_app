from django.urls import path

from apps.restaurants.views.restaurant import RestaurantListView, RestaurantDetailView
from apps.restaurants.views.bookmark import BookmarkView
from apps.restaurants.views.visited import VisitedView

app_name = "restaurants"
urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant_list"),
    path("<int:id>/", RestaurantDetailView.as_view(), name="restaurant_detail"),
    path(
        "restaurants/<int:restaurant_id>/bookmark/",
        BookmarkView.as_view(),
        name="restaurant-bookmark",
    ),
    path(
        "restaurants/<int:restaurant_id>/visited/",
        VisitedView.as_view(),
        name="restaurant-visited",
    ),
]
