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

    path('text_ext', views.text_ext, name='text-ext'),
    # path('payment', views.payment, name='payment'),
    path("payment/", views.payment_form, name="payment_form"),
    # path("payment/success/", views.payment_success, name="payment_success"),
    # path("payment/failure/", views.payment_failure, name="payment_failure"),


    path("shop/", views.product_list, name="product_list"),
    path("cart/", views.view_cart, name="view_cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("update/<int:item_id>/", views.update_quantity, name="update_quantity"),
    path("checkout/", views.checkout, name="checkout"),
    path('shop/payment_success/', views.payment_success, name='payment_success'),
    path('shop/payment_failed/', views.payment_failed, name='payment_failed'),

]
