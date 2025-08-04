from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Experience(models.Model):
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    years = models.IntegerField()

    def __str__(self):
        return f"{self.position} at {self.company}"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"