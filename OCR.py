# OCR.py

import os
import tempfile
import ocrmypdf
from PyPDF2 import PdfReader

def is_soft_copy(pdf_file):
    try:
        pdf_reader = PdfReader(pdf_file)
        # Loop through each page and check for text
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:  # If any text is found, it's a soft copy
                return True
        return False  # No text found, likely hard copy
    except Exception as e:
        return False

# Default OCR language
DEFAULT_LANGUAGE = "eng"

# Function to perform OCR on PDF files
def perform_ocr(pdf_files, language=DEFAULT_LANGUAGE):
    temp_dir = tempfile.mkdtemp()
    ocr_results = []

    # Perform OCR on each uploaded PDF
    for pdf_file in pdf_files:
        input_path = os.path.join(temp_dir, pdf_file.name)
        output_path = os.path.join(temp_dir, f"OCR_{pdf_file.name}")

        # Save uploaded file to temporary directory
        with open(input_path, "wb") as f:
            f.write(pdf_file.read())

        # Perform OCR
        ocrmypdf.ocr(
            input_path,
            output_path,
            language=language,
            force_ocr=True
        )

        ocr_results.append(output_path)

    return ocr_results

