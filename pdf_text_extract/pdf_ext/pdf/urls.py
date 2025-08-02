from .views import home, extract_pdf_text
from django.urls import path, include
urlpatterns = [
    path('', home, name='home'),
    path('extract/', extract_pdf_text, name='extract_pdf_text'),
]
