import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .face_auth import FaceAuthenticator
from .models import LoginHistory, User

# Initialize face authenticator
face_auth = FaceAuthenticator()


def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def login_page(request):
    """Display the login page with face authentication button"""
    return render(request, "authentication/login.html")


def home_page(request):
    """Home page after successful authentication"""
    if request.session.get("authenticated"):
        user_name = request.session.get("user_name", "User")
        return render(request, "authentication/home.html", {"user_name": user_name})
    else:
        messages.error(request, "Please authenticate first.")
        return redirect("login")


@csrf_exempt
def authenticate_face(request):
    """Handle face authentication via AJAX"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            image_data = data.get("image")

            if not image_data:
                return JsonResponse({"success": False, "message": "No image provided"})

            # Authenticate face
            is_authenticated, result = face_auth.authenticate_face(image_data)

            if is_authenticated:
                # Get or create user in database
                user, created = User.objects.get_or_create(
                    username=result, defaults={"authenticated": True, "login_count": 0}
                )
                

                # Record login
                user.record_login()

                # Create login history entry
                LoginHistory.objects.create(
                    user=user, ip_address=get_client_ip(request), success=True
                )

                # Set session variables
                request.session["authenticated"] = True
                request.session["user_name"] = result
                request.session["user_id"] = user.id

                return JsonResponse(
                    {
                        "success": True,
                        "message": f"Authentication successful! Welcome {result}",
                        "redirect_url": "/home/",
                    }
                )
            else:
                # Record failed login attempt
                LoginHistory.objects.create(
                    user=None,  # No user for failed attempts
                    ip_address=get_client_ip(request),
                    success=False,
                )

                return JsonResponse(
                    {"success": False, "message": f"Authentication failed: {result}"}
                )

        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Error processing request: {str(e)}"}
            )

    return JsonResponse({"success": False, "message": "Invalid request method"})


def logout(request):
    """Logout user and clear session"""
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect("login")
