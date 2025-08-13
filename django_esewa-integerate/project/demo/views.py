from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.core.files.storage import default_storage
import os
from .azure_llm import extract_data_from_llm
from .pdf_extract import extract_text_from_pdf
from .models import UserData




User = get_user_model() 

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('signin')


def signin(request):
    return render(request, 'signin.html')


def demo(request):
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error, extra_tags='signup')
            return redirect('signin')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.", extra_tags='signup')
            return redirect('signin')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created. Please log in.", extra_tags='login')
        return redirect('signin')

    return redirect('signin')


from django.template.context_processors import csrf

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST['email']
        password = request.POST['password']

        user = None
        try:
            user_obj = User.objects.get(email=identifier)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username/email or password')
            context = {}
            context.update(csrf(request))
            return render(request, 'signin.html', context)

    return redirect('signin')

def redirect_to_signin(request):
    return redirect('signin')



otp_store = {}

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            otp_store[email] = otp

            # Send OTP
            send_mail(
                'Your Password Reset OTP',
                f'Your OTP is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            request.session['reset_email'] = email
            messages.success(request, 'OTP sent to your email.')
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'Email is not registered.')
            return redirect('password/forgot_password')
    return render(request, 'password/forgot_password.html')


def verify_otp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        entered_otp = request.POST.get('otp')

        if email and otp_store.get(email) == int(entered_otp):
            messages.success(request, 'OTP verified. Please reset your password.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP.')
            return redirect('verify_otp')
    return render(request, 'password/verify_otp.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        new_password = request.POST.get('password')

        # Validate new password
        try:
            validate_password(new_password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('reset_password')

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            otp_store.pop(email, None)
            request.session.pop('reset_email', None)
            messages.success(request, 'Password reset successful.')
            return redirect('signin')
        except User.DoesNotExist:
            messages.error(request, 'Something went wrong.')
            return redirect('forgot_password')
    return render(request, 'password/reset_password.html')


def text_ext(request):
    extracted_data = None

    if request.method == "POST" and request.FILES.get("pdf_user"):
        pdf_file = request.FILES["pdf_user"]

        pdf_text = extract_text_from_pdf(pdf_file)
        extracted_data = extract_data_from_llm(pdf_text)

        if extracted_data:
            UserData.objects.create(
                name=extracted_data.get("name"),
                address=extracted_data.get("address"),
                phone=extracted_data.get("phone"),
                education=extracted_data.get("education"),
                experience=extracted_data.get("experience", ""),
                skills=extracted_data.get("skills", []),
                projects=extracted_data.get("projects", []),
                extracted_text=pdf_text,  # save raw extracted text here
            )

    return render(request, "text_ext.html", {"extracted_data": extracted_data})



# def payment(request):
#     return render(request, 'payment.html')


import hmac
import hashlib
import base64
import uuid
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse


def generate_signature(fields: dict, signed_field_names: str, secret_key: str) -> str:
    """
    Generate eSewa HMAC SHA256 signature in base64 format.
    Fields must match the signed_field_names order.
    """
    message = ",".join(f"{name}={fields[name]}" for name in signed_field_names.split(","))
    hmac_sha256 = hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)
    return base64.b64encode(hmac_sha256.digest()).decode("utf-8")


def payment_form(request):
    config = settings.ESEWA_CONFIG
    
    amount = request.session.get("checkout_total", 100.00)  # default for testing
    tax_amount = 0.00
    product_service_charge = 0.00
    product_delivery_charge = 0.00
    total_amount = amount + tax_amount + product_service_charge + product_delivery_charge

    transaction_uuid = str(uuid.uuid4())

    signed_field_names = "total_amount,transaction_uuid,product_code"
    signature_fields = {
        "total_amount": str(total_amount),
        "transaction_uuid": transaction_uuid,
        "product_code": config["PRODUCT_CODE"],
    }
    signature = generate_signature(signature_fields, signed_field_names, config["SECRET_KEY"])

    context = {
        "test_url": config["TEST_URL"],
        "amount": amount,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
        "product_code": config["PRODUCT_CODE"],
        "product_service_charge": product_service_charge,
        "product_delivery_charge": product_delivery_charge,
        "success_url": config["SUCCESS_URL"],
        "failure_url": config["FAILURE_URL"],
        "signed_field_names": signed_field_names,
        "signature": signature,
    }
    return render(request, "payment.html", context)





from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "shop/product_list.html", {"products": products})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=1)

    messages.success(request, f"{product.name} added to cart!")

    # Re-render the product list page
    products = Product.objects.all()
    return render(request, "shop/product_list.html", {"products": products})



@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "shop/cart.html", {"cart": cart})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("view_cart")


@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
    return redirect("view_cart")


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    total = cart.total_amount  # <-- no parentheses

    # save total in session for payment
    request.session["checkout_total"] = float(total)
    return redirect("payment_form")



from django.views.decorators.csrf import csrf_exempt

from .models import Order, Cart, CartItem

@login_required(login_url='signin')
@csrf_exempt
def payment_success(request):
    """
    Handle successful payment from eSewa and create the Order.
    """
    # Grab GET params from eSewa
    payment_data = request.GET.dict()
    print("Payment Success Data:", payment_data)

    # Get user's cart
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "No items in cart.")
        return redirect("product_list")

    # Create Order
    order = Order.objects.create(
        user=request.user,
        total_amount=cart.total_amount(),
        payment_status='Completed',  # optional field in Order model
        transaction_id=payment_data.get("transaction_uuid", ""),
    )

    # Move items from cart to order
    for item in cart.items.all():
        order.items.create(
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # Clear cart
    cart.items.all().delete()

    return render(request, "shop/payment_success.html", {"order": order})


from django.contrib.auth import get_user_model
User = get_user_model()


@login_required(login_url='signin')
@csrf_exempt
def payment_failed(request):
    """
    Handle failed payment from eSewa.
    """
    payment_data = request.GET.dict()
    print("Payment Failed Data:", payment_data)

    return render(request, "shop/payment_failed.html", {"payment_data": payment_data})


