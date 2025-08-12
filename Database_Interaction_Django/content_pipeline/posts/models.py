from django.db import models
from pathlib import Path
import pdfplumber

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to="pdfs/", blank=True, null=True)
    text_file = models.FileField(upload_to="texts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def extract_pdf_to_text(self):
        """Extracts text from uploaded PDF and saves it as a .txt file."""
        if self.pdf_file:
            pdf_path = Path(self.pdf_file.path)
            output_text_path = pdf_path.with_suffix(".txt").name
            text_output_full_path = Path(self.pdf_file.storage.location) / "texts" / output_text_path
            
            # Ensure output directory exists
            text_output_full_path.parent.mkdir(parents=True, exist_ok=True)

            # Extract PDF text
            with pdfplumber.open(pdf_path) as pdf:
                extracted_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    extracted_text += page_text if page_text else "[No text found]\n"

            # Save to .txt file
            with open(text_output_full_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)

            # Save relative path to model
            self.text_file.name = f"texts/{output_text_path}"
            self.save()
