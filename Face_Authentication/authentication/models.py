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
