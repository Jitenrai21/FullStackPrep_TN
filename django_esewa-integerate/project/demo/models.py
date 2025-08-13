# user/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission 
from django.db import models
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    mfa_secret = models.CharField(max_length=16, blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.email



class UserData(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    education = models.JSONField(null=True, blank=True) 
    experience = models.CharField(max_length=255, null=True, blank=True)
    skills = models.JSONField(null=True, blank=True) 
    projects = models.JSONField(null=True, blank=True)
    extracted_text = models.TextField(null=True, blank=True)  # new field for full extracted text

    def __str__(self):
        return self.name




from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    payment_status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
