import pdfplumber

def read_pdf(file_path):
    """Membaca seluruh teks dari file PDF"""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error membaca PDF: {e}")
        return ""

# Contoh penggunaan
pdf_text = read_pdf("dokumen1.pdf")
print(pdf_text[:500])