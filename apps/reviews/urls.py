from django.urls import path
from apps.reviews.views import ReviewSubmitView, ReviewDeleteView

app_name = "reviews"

urlpatterns = [
    path(
        "restaurant/<int:restaurant_id>/submit/",
        ReviewSubmitView.as_view(),
        name="submit",
    ),
    path(
        "<int:review_id>/delete/",
        ReviewDeleteView.as_view(),
        name="delete",
    ),
]
