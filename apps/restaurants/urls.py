from django.urls import path

from apps.restaurants.views import RestaurantListView, RestaurantDetailView

app_name = "restaurants"
urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant_list"),
    path("<int:id>/", RestaurantDetailView.as_view(), name="restaurant_detail"),
]
