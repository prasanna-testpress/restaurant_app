from django.shortcuts import get_object_or_404

from django.views.generic import ListView, DetailView

from apps.restaurants.models import Restaurant, Cuisine,MenuItem, RestaurantImage
from django.db.models import Avg, Count, Prefetch
from apps.reviews.models import Review

from apps.restaurants.filters import RestaurantFilter

from apps.restaurants.domain import is_restaurant_bookmarked

class RestaurantListView(ListView):
    template_name = "restaurants/list.html"
    context_object_name = "restaurants"
    paginate_by = 10

    def get_queryset(self):
        self.filterset = RestaurantFilter(
            data=self.request.GET,
            queryset=Restaurant.objects.prefetch_related(
                "images",
                "cuisines",
            ),
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        base_qs = self.filterset.qs

        context["spotlight_restaurants"] = base_qs.filter(is_spotlight=True)
       
        context["filter"] = self.filterset

        context["cities"] = (
            Restaurant.objects
            .values_list("city", flat=True)
            .distinct()
            .order_by("city")
        )

        context["cuisines"] = (
            Cuisine.objects
            .values_list("name", flat=True)
            .distinct()
            .order_by("name")
        )

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params

        return context



class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "restaurant/detail.html"
    context_object_name = "restaurant"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        return get_object_or_404(
            _get_restaurant_detail_queryset(),
            id=self.kwargs["id"],
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = context["restaurant"]
        user = self.request.user

        if user.is_authenticated:
            context["is_bookmarked"] = is_restaurant_bookmarked(
                user=user,
                restaurant_id=restaurant.id,
            )
            
        else:
            context["is_bookmarked"] = False

        return context

def _get_restaurant_detail_queryset():
    """
    Helper function for RestaurantDetailView.
    Encapsulates complex query logic.
    """
    return (
        Restaurant.objects
        .prefetch_related(
            "cuisines",
            Prefetch(
                "menu_items",
                queryset=MenuItem.objects.order_by("name"),
            ),
            Prefetch(
                "images",
                queryset=RestaurantImage.objects.order_by("uploaded_at"),
            ),
            Prefetch(
                "reviews",
                queryset=Review.objects
                .select_related("user")
                .order_by("-created_at"),
            ),
        )
        .annotate(
            avg_rating=Avg("reviews__rating"),
            review_count=Count("reviews"),
        )
    )
