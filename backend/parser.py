"""
parser.py
---------
Handles PDF text extraction for MediScan.
Uses pdfplumber to extract structured table data first,
then falls back to raw text extraction if no tables are found.
"""

import io
import pdfplumber


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text content from a PDF file provided as raw bytes.

    Attempts table extraction first for structured lab reports.
    Falls back to raw text extraction if no tables are detected.

    Args:
        file_bytes: Raw bytes of the uploaded PDF file.

    Returns:
        A single string containing all extracted text from the PDF.

    Raises:
        ValueError: If the file is not a valid PDF, is encrypted,
                    or yields no extractable content.
    """
    if not file_bytes:
        raise ValueError("Empty file provided. Please upload a valid PDF.")

    if not file_bytes.startswith(b"%PDF"):
        raise ValueError("Uploaded file does not appear to be a valid PDF.")

    try:
        pdf_stream = io.BytesIO(file_bytes)
        extracted_parts = []

        with pdfplumber.open(pdf_stream) as pdf:
            if pdf.pages == []:
                raise ValueError("The PDF contains no pages.")

            for page_num, page in enumerate(pdf.pages, start=1):
                # --- Attempt table extraction ---
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        for row in table:
                            if row:
                                cleaned_row = "\t".join(
                                    cell.strip() if cell else ""
                                    for cell in row
                                )
                                if cleaned_row.strip():
                                    extracted_parts.append(cleaned_row)
                else:
                    # --- Fall back to raw text extraction ---
                    raw_text = page.extract_text()
                    if raw_text:
                        extracted_parts.append(raw_text.strip())

        if not extracted_parts:
            raise ValueError(
                "No text could be extracted from this PDF. "
                "It may be a scanned image PDF or contain only graphics."
            )

        return "\n".join(extracted_parts)

    except pdfplumber.pdfminer.pdfparser.PDFSyntaxError:
        raise ValueError("The PDF file is corrupted or uses an unsupported format.")
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Failed to process PDF: {str(e)}")