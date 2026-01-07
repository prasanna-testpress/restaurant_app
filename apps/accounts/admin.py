from django.contrib import admin
from .models import Bookmark, Visited
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["user", "restaurant", "created_at"]
    search_fields = ["user__username", "restaurant__name"]


@admin.register(Visited)
class VisitedAdmin(admin.ModelAdmin):
    list_display = ["user", "restaurant", "visited_at"]
    search_fields = ["user__username", "restaurant__name"]

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "is_staff", "is_active", "created_at"]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["email"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    readonly_fields = ["created_at", "last_login"]