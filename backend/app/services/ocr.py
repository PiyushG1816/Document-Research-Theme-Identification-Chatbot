import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    pages = []
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text()
        if not text.strip():
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)
        pages.append((page_num + 1, text))
    return pages

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return [(1, text)]
