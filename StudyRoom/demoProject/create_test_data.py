#!/usr/bin/env python
import os

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demoProject.settings")
django.setup()

from demoapp.models import Room
from django.contrib.auth.models import User

# Create admin user
admin_user, created = User.objects.get_or_create(
    username="admin",
    defaults={"email": "admin@example.com", "first_name": "Admin", "last_name": "User"},
)
if created:
    admin_user.set_password("admin123")
    admin_user.save()
    print("✅ Created admin user (username: admin, password: admin123)")
else:
    print("ℹ️  Admin user already exists")

# Create test rooms
rooms = [
    {
        "name": "Python Basics",
        "description": "Learn Python fundamentals and basic programming concepts",
        "type": "free",
    },
    {
        "name": "Advanced AI & ML",
        "description": "Machine Learning and AI with premium chatbot support",
        "type": "premium",
    },
    {
        "name": "Web Development",
        "description": "HTML, CSS, JavaScript and Django web development",
        "type": "free",
    },
    {
        "name": "Data Science Pro",
        "description": "Professional data science with premium voice features",
        "type": "premium",
    },
]

print("\n🏠 Creating test rooms...")
for room_data in rooms:
    room, created = Room.objects.get_or_create(
        name=room_data["name"],
        defaults={
            "description": room_data["description"],
            "type": room_data["type"],
            "created_by": admin_user,
        },
    )
    if created:
        print(f"✅ Created: {room.name} ({room.type})")
    else:
        print(f"ℹ️  Already exists: {room.name}")

print(f"\n📊 Total rooms in database: {Room.objects.count()}")
print("\n🚀 You can now visit http://127.0.0.1:8000/rooms/ to see the rooms!")
