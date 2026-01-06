from django.contrib import admin

from .models import Bookmark, Visited


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["user", "restaurant", "created_at"]
    search_fields = ["user__email", "restaurant__name"]


@admin.register(Visited)
class VisitedAdmin(admin.ModelAdmin):
    list_display = ["user", "restaurant", "visited_at"]
    search_fields = ["user__email", "restaurant__name"]
