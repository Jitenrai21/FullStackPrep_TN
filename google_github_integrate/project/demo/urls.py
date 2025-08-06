from django.urls import path, re_path
from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('demo', views.demo, name='demo'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    re_path(r'^accounts/3rdparty/login/cancelled/$', views.redirect_to_signin),
]
