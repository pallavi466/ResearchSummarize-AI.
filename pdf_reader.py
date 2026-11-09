
import pdfplumber


def extract_text(pdf_path):
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

    if not extracted_text.strip():
        raise ValueError(
            "No readable text found in PDF. "
            "The PDF may contain scanned images."
        )

    return extracted_text
