from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('add_skill/', views.add_skill, name='add_skill'),
    path('add_experience/', views.add_experience, name='add_experience'),
        # The URL to load the HTML page (e.g., http://127.0.0.1:8000/tracker/)
    path('tracker/', views.tracker_page, name='tracker_page'),

    # The URL for the JavaScript to make a POST request to (e.g., http://127.0.0.1:8000/process_frame/)
    path('process_frame/', views.process_frame, name='process_frame_api'),
    path('assistant/', views.voice_assistant_page, name='assistant'),
    path('initialize/', views.initialize, name='initialize'),
    path('process_command/', views.process_command, name='process_command'),
]