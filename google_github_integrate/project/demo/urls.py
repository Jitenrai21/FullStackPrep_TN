from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),   # Add this for the signin page
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    re_path(r'^accounts/3rdparty/login/cancelled/$', views.redirect_to_signin),
]
