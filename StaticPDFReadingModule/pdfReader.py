import pdfplumber
from pathlib import Path

def extract_text_with_pdfplumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            # text += f"\n--- Page {i + 1} ---\n"
            text += page_text if page_text else "[No text found]\n"
    return text

def save_text_to_file(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Text successfully saved to '{output_path}'")

# Example usage
if __name__ == "__main__":
    base_dir = Path(__file__).parent.resolve()
    pdf_path = "JitenRaiCV.pdf"
    result = extract_text_with_pdfplumber(pdf_path)
    print(result)
    # output_txt_path = 'Extracted_file.txt'
    # save_text_to_file(result, output_txt_path)