import base64
import hashlib
import hmac
import json

import requests
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(
    directory="templates"
)  # Assumes templates are in a 'templates' folder

# eSewa configuration
SECRET_KEY = "8gBm/:&EnhH.1/q"
PRODUCT_CODE = "EPAYTEST"
TEST_URL = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
SUCCESS_URL = "http://localhost:8000/success"
FAILURE_URL = "http://localhost:8000/failure"
# https://rc-epay.esewa.com.np/api/epay/main/v2/form

# hmac_sha256 = hmac.new(secret, message, hashlib.sha256)
# digest = hmac_sha256.digest()
# signature = base64.b64encode(digest).decode('utf-8')


def generate_signature_from_fields(fields: dict, signed_field_names: str) -> str:
    """
    Generate HMAC SHA256 signature in base64 as per eSewa documentation.
    The message is a comma-separated string of the values of signed_field_names in order.
    """
    # Create the message string in the exact order of signed_field_names
    # e.g., 'total_amount=100,transaction_uuid=11-201-13,product_code=EPAYTEST'
    message = ",".join(
        f"{name}={fields[name]}" for name in signed_field_names.split(",")
    )
    secret_bytes = SECRET_KEY.encode("utf-8")
    message_bytes = message.encode("utf-8")
    hmac_sha256 = hmac.new(secret_bytes, message_bytes, hashlib.sha256)
    digest = hmac_sha256.digest()
    return base64.b64encode(digest).decode("utf-8")


@app.get("/", response_class=HTMLResponse)
async def payment_form(request: Request):
    # Example values; in production, get these from user input or order system
    amount = "100"
    tax_amount = "10"
    product_service_charge = "0"
    product_delivery_charge = "0"
    total_amount = str(
        float(amount)
        + float(tax_amount)
        + float(product_service_charge)
        + float(product_delivery_charge)
    )
    transaction_uuid = "141329"  # Should be unique per transaction in production
    signed_field_names = "total_amount,transaction_uuid,product_code"
    # Only these fields are used for signature, as per documentation
    signature_fields = {
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
        "product_code": PRODUCT_CODE,
    }
    signature = generate_signature_from_fields(signature_fields, signed_field_names)
    # Render the form using Jinja2 template
    return templates.TemplateResponse(
        "payment_form.html",
        {
            "request": request,
            "test_url": TEST_URL,
            "amount": amount,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "transaction_uuid": transaction_uuid,
            "product_code": PRODUCT_CODE,
            "product_service_charge": product_service_charge,
            "product_delivery_charge": product_delivery_charge,
            "success_url": SUCCESS_URL,
            "failure_url": FAILURE_URL,
            "signed_field_names": signed_field_names,
            "signature": signature,
        },
    )


@app.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    return "Payment Successful!"


@app.get("/failure", response_class=HTMLResponse)
async def failure():
    return "Payment Failed. Please try again."
