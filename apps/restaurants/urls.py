from django.urls import path

from apps.restaurants.views import (
    RestaurantListView,
    RestaurantDetailView,
    BookmarkToggleView,
    VisitedToggleView,
    MyActivityView,
    MyBookmarksView,
    MyVisitedView,
)


app_name = "restaurants"
urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant_list"),
    path("<int:id>/", RestaurantDetailView.as_view(), name="restaurant_detail"),
    path("<int:restaurant_id>/bookmark/", BookmarkToggleView.as_view(), name="bookmark"),
    path("<int:restaurant_id>/visited/", VisitedToggleView.as_view(), name="visited"),
    path("my-activity/", MyActivityView.as_view(), name="my_activity"),
    path("my-activity/bookmarks/", MyBookmarksView.as_view(), name="my_bookmarks"),
    path("my-activity/visited/", MyVisitedView.as_view(), name="my_visited"),

]
