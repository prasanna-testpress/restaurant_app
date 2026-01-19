from apps.accounts.models import Bookmark, Visited

def is_restaurant_bookmarked(*, user, restaurant_id: int) -> bool:
    return Bookmark.objects.filter(
        user=user,
        restaurant_id=restaurant_id,
    ).exists()

def is_restaurant_visited(*, user, restaurant_id: int) -> bool:
    return Visited.objects.filter(
        user=user,
        restaurant_id=restaurant_id,
    ).exists()

