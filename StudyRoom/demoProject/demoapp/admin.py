from django.contrib import admin

from .models import Room, RoomMember, UserProfile

# Register your models here.


# models register in admin pannel : samirdahal
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "created_by", "created_at"]
    list_filter = ["type", "created_at"]
    search_fields = ["name", "description"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "age"]
    search_fields = ["user__username", "user__email", "phone"]


@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ["user", "room", "status", "joined_at"]
    list_filter = ["status", "joined_at"]
    search_fields = ["user__username", "room__name"]


# end samirdahal
