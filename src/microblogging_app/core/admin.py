from typing import Any

from core.models import Like, Notification, NotificationType, Repost, Tag, Tweet, User
from django.contrib import admin
from django.utils.safestring import mark_safe


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "get_html_photo",
        "email",
        "first_name",
        "last_name",
        "description",
        "birth_date",
        "country",
        "is_staff",
        "last_login",
        "is_active",
        "created_at",
    ]
    list_display_links = ["id", "username"]
    list_editable = ["is_active"]
    filter_horizontal = ["following"]
    ordering = ["created_at", "is_active"]
    fields = [
        "username",
        "email",
        "is_active",
        "first_name",
        "last_name",
        "description",
        "birth_date",
        "country",
        "is_staff",
        "last_login",
        "created_at",
        "get_html_photo",
        "following",
    ]
    readonly_fields = ["created_at", "updated_at", "get_html_photo"]
    list_per_page = 10

    @admin.decorators.display(description="User photo")
    def get_html_photo(self, object: User) -> Any | None:
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")
        else:
            return None


class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    list_display_links = ["id", "name"]
    ordering = ["id"]
    list_per_page = 10


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "message", "notification_type", "created_at"]
    list_display_links = ["id"]
    list_per_page = 10
    list_filter = ["notification_type"]
    ordering = ["created_at"]
    filter_horizontal = ["user"]


class TweetAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "reply_to", "user", "created_at"]
    list_display_links = ["id"]
    ordering = ["created_at", "reply_to"]
    list_per_page = 10
    filter_horizontal = ["tags", "repost", "like"]


class RepostAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "tweet", "created_at"]
    list_display_links = ["id"]
    ordering = ["created_at"]
    list_per_page = 10


class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    list_display_links = ["id", "name"]
    ordering = ["created_at"]
    list_per_page = 10


class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "tweet", "created_at"]
    list_display_links = ["id"]
    ordering = ["created_at"]
    list_per_page = 10


admin.site.register(Like, LikeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Repost, RepostAdmin)
admin.site.register(NotificationType, NotificationTypeAdmin)
admin.site.register(Tweet, TweetAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Notification, NotificationAdmin)
