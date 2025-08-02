import pdfplumber
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def extract_pdf_text(request):
    if request.method == 'POST' and request.FILES.get('pdfFile'):
        pdf_file = request.FILES['pdfFile']
        path = default_storage.save(pdf_file.name, pdf_file)
        full_path = default_storage.path(path)

        text = ""
        with pdfplumber.open(full_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                text += page_text if page_text else "[No text found]\n"

        return JsonResponse({'text': text})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
