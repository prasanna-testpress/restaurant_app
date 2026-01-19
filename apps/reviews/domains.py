from django.shortcuts import get_object_or_404
from typing import Optional

from apps.reviews.models import Review
from apps.restaurants.models import Restaurant
from django.contrib.auth import get_user_model

User = get_user_model()

def get_user_review_for_restaurant(*, user: User, restaurant: Restaurant) -> Optional[Review]:
    return Review.objects.filter(user=user, restaurant=restaurant).first()





def delete_review(*, user: User, review_id: int) -> int:
    review = get_object_or_404(
            Review,
            id=review_id,
            user=user,
        )

    restaurant_id = review.restaurant_id
    review.delete()

    return restaurant_id