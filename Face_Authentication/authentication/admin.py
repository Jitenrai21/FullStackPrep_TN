import os

import face_recognition
from django.contrib import admin, messages
from django.forms import FileField, ModelForm
from django.utils.html import format_html

from .models import FaceEmbedding, LoginHistory, User

# Register your models here.


class FaceEmbeddingForm(ModelForm):
    """Custom form for FaceEmbedding with image upload"""

    image_file = FileField(
        required=True,
        help_text="Upload a clear image of the person's face (JPG or JPEG format)",
    )

    class Meta:
        model = FaceEmbedding
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["image_file"].required = False
            self.fields[
                "image_file"
            ].help_text = "Upload a new image to replace the existing one"


@admin.register(FaceEmbedding)
class FaceEmbeddingAdmin(admin.ModelAdmin):
    """Admin interface for Face Embeddings - Only accessible by superusers"""

    form = FaceEmbeddingForm
    list_display = [
        "name",
        "image_filename",
        "created_at",
        "updated_at",
        "image_preview",
    ]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["name", "image_filename"]
    readonly_fields = ["embedding_data", "created_at", "updated_at", "image_preview"]

    fieldsets = (
        ("Person Information", {"fields": ("name", "image_file")}),
        (
            "System Information",
            {
                "fields": ("image_filename", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
        ("Technical Data", {"fields": ("embedding_data",), "classes": ("collapse",)}),
    )

    def has_module_permission(self, request):
        """Only superusers can access this module"""
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Only superusers can view face embeddings"""
        return request.user.is_superuser

    def has_add_permission(self, request):
        """Only superusers can add face embeddings"""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Only superusers can change face embeddings"""
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete face embeddings"""
        return request.user.is_superuser

    def image_preview(self, obj):
        """Display a preview of the uploaded image"""
        if obj.image_filename:
            image_path = f"known_faces/{obj.image_filename}"
            if os.path.exists(image_path):
                return format_html(
                    '<img src="/images/{}" width="100" height="100" style="object-fit: cover;" />',
                    obj.image_filename,
                )
        return "No image"

    image_preview.short_description = "Image Preview"

    def save_model(self, request, obj, form, change):
        """Process the uploaded image and generate face embedding"""

        if "image_file" in form.cleaned_data and form.cleaned_data["image_file"]:
            uploaded_file = form.cleaned_data["image_file"]

            # Validate file type
            if not uploaded_file.name.lower().endswith((".jpg", ".jpeg")):
                messages.error(request, "Please upload a JPG or JPEG image file.")
                return

            # Create filename based on person's name
            file_extension = os.path.splitext(uploaded_file.name)[1]
            filename = f"{obj.name.replace(' ', '_')}{file_extension}"

            # Ensure known_faces directory exists
            known_faces_dir = "known_faces"
            if not os.path.exists(known_faces_dir):
                os.makedirs(known_faces_dir)

            # Save image to known_faces directory
            file_path = os.path.join(known_faces_dir, filename)

            # Remove old image if it exists
            if change and obj.image_filename:
                old_path = os.path.join(known_faces_dir, obj.image_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)

            # Save new image
            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Generate face embedding
            try:
                image = face_recognition.load_image_file(file_path)
                face_encodings = face_recognition.face_encodings(image)

                if not face_encodings:
                    messages.error(
                        request,
                        "No face detected in the uploaded image. Please upload a clear image with a visible face.",
                    )
                    # Remove the saved file
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    return

                if len(face_encodings) > 1:
                    messages.warning(
                        request,
                        "Multiple faces detected. Using the first detected face.",
                    )

                # Use the first face encoding
                face_encoding = face_encodings[0]

                # Update object with new data
                obj.image_filename = filename
                obj.set_embedding(face_encoding)

                messages.success(
                    request, f"Face embedding generated successfully for {obj.name}!"
                )

            except Exception as e:
                messages.error(request, f"Error processing image: {str(e)}")
                # Remove the saved file
                if os.path.exists(file_path):
                    os.remove(file_path)
                return

        super().save_model(request, obj, form, change)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""

    list_display = [
        "username",
        "email",
        "authenticated",
        "login_count",
        "last_login",
        "created_at",
    ]
    list_filter = ["authenticated", "created_at", "last_login"]
    search_fields = ["username", "email"]
    readonly_fields = ["created_at", "last_login", "login_count"]


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    """Admin interface for Login History"""

    list_display = ["user", "login_time", "ip_address", "success"]
    list_filter = ["success", "login_time"]
    search_fields = ["user__username", "ip_address"]
    readonly_fields = ["login_time"]
