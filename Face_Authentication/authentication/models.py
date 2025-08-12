from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):  # Fixed: models.Model not models.MModel
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    authenticated = models.BooleanField(default=False)
    login_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    def record_login(self):
        """Update login info when user successfully logs in"""
        self.authenticated = True
        self.last_login = timezone.now()
        self.login_count += 1
        self.save()


class LoginHistory(models.Model):
    """Track each login attempt"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="login_history"
    )
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    success = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

    # add admin panel name for this
    class Meta:
        verbose_name_plural = "Login Histories"


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
        import json

        import numpy as np

        return np.array(json.loads(self.embedding_data))
