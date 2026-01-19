from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from apps.reviews.forms import ReviewForm
from apps.reviews.models import Review
from apps.restaurants.models import Restaurant
from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewSubmitView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id, *args, **kwargs):
        form = ReviewForm(request.POST)

        if not form.is_valid():
            return redirect("restaurants:restaurant_detail", id=restaurant_id)

        self._submit_review(
            user=request.user,
            restaurant_id=restaurant_id,
            rating=form.cleaned_data["rating"],
            comment=form.cleaned_data["comment"],
        )
        return redirect("restaurants:restaurant_detail", id=restaurant_id)

        
    def _submit_review(self, user: User, restaurant_id: int, rating: int, comment: str) -> Review:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        review, _ = Review.objects.update_or_create(
            user=user,
            restaurant=restaurant,
            defaults={
                "rating": rating,
                "comment": comment,
            },
        )
        return review


class ReviewDeleteView(LoginRequiredMixin, View):
    def post(self, request, review_id, *args, **kwargs):
        restaurant_id = self._delete_review(
            user=request.user,
            review_id=review_id,
        )
        return redirect("restaurants:restaurant_detail", id=restaurant_id)

    def _delete_review(self, user: User, review_id: int) -> int:
        review = get_object_or_404(
                Review,
                id=review_id,
                user=user,
            )

        restaurant_id = review.restaurant_id
        review.delete()

        return restaurant_id
        