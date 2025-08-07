from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_page, name="login"),
    path("home/", views.home_page, name="home"),
    path("authenticate/", views.authenticate_face, name="authenticate_face"),
    path("logout/", views.logout, name="logout"),
]
