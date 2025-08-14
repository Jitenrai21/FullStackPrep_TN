from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # samirdahal
    path("rooms/", views.rooms_list, name="rooms_list"),
    path(
        "rooms/<int:room_id>/select-plan/",
        views.room_plan_select,
        name="room_plan_select",
    ),
    path("rooms/<int:room_id>/join-free/", views.join_free_room, name="join_free_room"),
    path(
        "rooms/<int:room_id>/join-premium/",
        views.join_premium_room,
        name="join_premium_room",
    ),
    path("rooms/<int:room_id>/face-auth/", views.face_auth, name="face_auth"),
    path("rooms/<int:room_id>/", views.room_detail, name="room_detail"),
    # end samirdahal
]
