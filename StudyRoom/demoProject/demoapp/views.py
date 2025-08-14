from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Room, RoomMember, UserProfile

# Create your views here.


def index(request):
    return render(request, "index.html")


# samir dahal
# @login_required
def rooms_list(request):
    """Display all available rooms"""
    rooms = Room.objects.all().order_by("-created_at")
    return render(request, "samir_templates/rooms_list.html", {"rooms": rooms})


# @login_required
def room_plan_select(request, room_id):
    """Show plan selection page for a room"""
    room = get_object_or_404(Room, id=room_id)

    # Check if user is already a member
    # existing_member = RoomMember.objects.filter(user=request.user, room=room).first()
    # if existing_member:
    #     if existing_member.status == "active":
    #         return redirect("room_detail", room_id=room.id)
    #     elif existing_member.status == "pending":
    #         messages.info(request, "Your membership is pending approval.")
    #         return redirect("rooms_list")

    return render(request, "samir_templates/room_plan_select.html", {"room": room})


# @login_required
def join_free_room(request, room_id):
    """Handle free room join form"""
    room = get_object_or_404(Room, id=room_id)

    if room.type != "free":
        messages.error(request, "This is not a free room.")
        return redirect("room_plan_select", room_id=room.id)

    if request.method == "POST":
        # Create test user if not authenticated (for testing purposes)
        if not request.user.is_authenticated:
            from django.contrib.auth.models import User

            test_user, created = User.objects.get_or_create(
                username="testuser1",
                defaults={
                    "email": "test@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                },
            )
            from django.contrib.auth import login

            login(request, test_user)

        # Get user profile or create one
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Update profile with form data
        profile.phone = request.POST.get("phone", "")
        age = request.POST.get("age")
        if age:
            profile.age = int(age)

        # Handle face image upload
        if "face_image" in request.FILES:
            profile.face_image = request.FILES["face_image"]

        profile.save()

        # Create room membership
        room_member, created = RoomMember.objects.get_or_create(
            user=request.user,
            room=room,
            defaults={"status": "pending"},  # Will go to face auth next
        )

        # Show success message
        messages.success(
            request, "Submitted successfully! Your application has been received."
        )
        return render(
            request,
            "samir_templates/free_join_form.html",
            {"room": room, "success": True},
        )

    return render(request, "samir_templates/free_join_form.html", {"room": room})


# @login_required
def join_premium_room(request, room_id):
    """Handle premium room join (payment + approval)"""
    room = get_object_or_404(Room, id=room_id)

    if room.type != "premium":
        messages.error(request, "This is not a premium room.")
        return redirect("room_plan_select", room_id=room.id)

    if request.method == "POST":
        # Create test user if not authenticated (for testing purposes)
        if not request.user.is_authenticated:
            from django.contrib.auth.models import User

            test_user, created = User.objects.get_or_create(
                username="testuser1",
                defaults={
                    "email": "test@example.com",
                    "first_name": "Test",
                    "last_name": "User1",
                },
            )
            from django.contrib.auth import login

            login(request, test_user)

        # Get user profile or create one
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Update profile with form data
        profile.phone = request.POST.get("phone", "")
        age = request.POST.get("age")
        if age:
            profile.age = int(age)

        # Handle face image upload
        if "face_image" in request.FILES:
            profile.face_image = request.FILES["face_image"]

        profile.save()

        # Create room membership (pending approval for premium)
        room_member, created = RoomMember.objects.get_or_create(
            user=request.user,
            room=room,
            defaults={"status": "pending", "is_admin_approved": False},
        )

        # Show success message
        messages.success(
            request,
            "Submitted successfully! Payment processed. Waiting for admin approval.",
        )
        return render(
            request,
            "samir_templates/premium_join_form.html",
            {"room": room, "success": True},
        )

    return render(request, "samir_templates/premium_join_form.html", {"room": room})


@login_required
def face_auth(request, room_id):
    """Face authentication page"""
    room = get_object_or_404(Room, id=room_id)
    room_member = get_object_or_404(RoomMember, user=request.user, room=room)

    if request.method == "POST":
        # Face authentication logic will go here
        # For now, just mark as active
        room_member.status = "active"
        room_member.save()

        messages.success(request, f"Welcome to {room.name}!")
        return redirect("room_detail", room_id=room.id)

    return render(request, "samir_templates/face_auth.html", {"room": room})


@login_required
def room_detail(request, room_id):
    """Room detail page for active members"""
    room = get_object_or_404(Room, id=room_id)

    # Check if user is an active member
    try:
        member = RoomMember.objects.get(user=request.user, room=room, status="active")
    except RoomMember.DoesNotExist:
        messages.error(request, "You are not an active member of this room.")
        return redirect("rooms_list")

    return render(
        request, "samir_templates/room_detail.html", {"room": room, "member": member}
    )


# samir dahal end
