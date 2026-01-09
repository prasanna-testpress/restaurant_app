from django.urls import path

from apps.restaurants.views import RestaurantListView

app_name = "restaurants"
urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant_list"),
]