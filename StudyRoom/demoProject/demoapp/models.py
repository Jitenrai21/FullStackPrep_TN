import json

import numpy as np
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# models for rooms :samir dahal
class Room(models.Model):
    ROOM_TYPES = [
        ("free", "Free"),
        ("premium", "Premium"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=ROOM_TYPES, default="free")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class UserProfile(models.Model):
    """User profile model to store additional user information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_image = models.ImageField(upload_to="face_images/", blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class RoomMember(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("pending", "Pending"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ["user", "room"]  # User can only join a room once

    def __str__(self):
        return f"{self.user.username} in {self.room.name} ({self.status})"


class FaceEmbedding(models.Model):
    """Model to store face embeddings for authentication"""

    name = models.CharField(max_length=100, unique=True, help_text="Name of the person")
    image_filename = models.CharField(
        max_length=255, help_text="Original filename of the uploaded image"
    )
    embedding_data = models.TextField(help_text="JSON serialized face embedding data")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "face_embeddings"
        verbose_name = "Face Embedding"
        verbose_name_plural = "Face Embeddings"

    def __str__(self):
        return f"{self.name} - {self.image_filename}"

    def set_embedding(self, embedding_array):
        """Convert numpy array to JSON string for storage"""
        import json

        import numpy as np

        self.embedding_data = json.dumps(embedding_array.tolist())

    def get_embedding(self):
        """Convert JSON string back to numpy array"""
        return np.array(json.loads(self.embedding_data))


# end samirdahal
