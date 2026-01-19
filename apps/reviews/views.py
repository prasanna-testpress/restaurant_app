from django.urls import reverse
from django.views.generic import FormView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.reviews.forms import ReviewForm
from apps.reviews.models import Review
from apps.restaurants.models import Restaurant
from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewSubmitView(LoginRequiredMixin, FormView):
    form_class = ReviewForm
    template_name = "reviews/review.html"

    def form_valid(self, form):
        self._submit_review(
            user=self.request.user,
            restaurant_id=self.kwargs["restaurant_id"],
            rating=form.cleaned_data["rating"],
            comment=form.cleaned_data["comment"],
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "restaurants:restaurant_detail",
            kwargs={"id": self.kwargs["restaurant_id"]},
        )
        
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


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    pk_url_kwarg = "review_id"

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse(
            "restaurants:restaurant_detail",
            kwargs={"id": self.object.restaurant_id},
        )
        