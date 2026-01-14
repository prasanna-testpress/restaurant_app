from apps.accounts.models import Bookmark

def is_restaurant_bookmarked(*, user, restaurant_id: int) -> bool:
    return Bookmark.objects.filter(
        user=user,
        restaurant_id=restaurant_id,
    ).exists()
