from django.contrib import admin

from apps.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "restaurant", "rating", "created_at"]
    list_filter = ["rating"]
    search_fields = ["user__email", "restaurant__name"]
