import os
import nltk
import pdfplumber
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===================================================
# SETUP & KONFIGURASI
# ===================================================

# Install NLTK stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Stopwords Indonesia dasar (NLTK)
stop_words = set(stopwords.words('indonesian'))

# Sastrawi stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Folder path
folder_path = "documents"

# ===================================================
# FUNGSI-FUNGSI
# ===================================================

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

# ---------------------------------------------------
# 1. Preprocessing fungsi
# ---------------------------------------------------
def preprocess(text):
    # Lowercase: mengubah semua huruf kapital menjadi huruf kecil
    text = text.lower()
    
    # Tokenization: memecah kata ke dalam bentuk array
    tokens = nltk.word_tokenize(text)
    
    # Remove stopwords: menghapus kata yang tidak mengandung makna
    tokens = [t for t in tokens if t not in stop_words]
    
    # Stemming: mengubah kata ke bentuk dasar
    stemmed = [stemmer.stem(t) for t in tokens]
    
    # Kembalikan ke format string
    return " ".join(stemmed)

# ===================================================
# MEMBACA DOKUMEN PDF
# ===================================================

# Get PDF Files
pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

# Count pdf files
jumlah_pdf = len(pdf_files)

# Read all PDF files
docs = []
doc_names = []
for pdf_file in pdf_files:
    file_path = os.path.join(folder_path, pdf_file)
    content = read_pdf(file_path)
    if content:
        docs.append(content)
        doc_names.append(pdf_file)

print()

# ===================================================
# 2. DOKUMEN DAN QUERY
# ===================================================

query = "aku mahasiswa, primakara adalah kampus"

# Preprocess semua
processed_docs = [preprocess(d) for d in docs]
processed_query = preprocess(query)

print("=== Preprocessed Documents ===")
for i, d in enumerate(processed_docs):
    print(f"{doc_names[i]}: {d}")

print("\n=== Preprocessed Query ===")
print(processed_query)

# ===================================================
# 3. TF-IDF
# ===================================================

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_docs + [processed_query])

doc_vectors = tfidf_matrix[:-1]
query_vector = tfidf_matrix[-1]

# ===================================================
# 4. COSINE SIMILARITY
# ===================================================

scores = cosine_similarity(query_vector, doc_vectors)[0]

print("\n=== Skor Relevansi ===")
for i, score in enumerate(scores):
    print(f"{doc_names[i]}: {score:.4f}")

# Ranking
ranking = sorted(list(enumerate(scores)), key=lambda x: x[1], reverse=True)

print("\n=== Ranking Dokumen ===")
for idx, score in ranking:
    print(f"{doc_names[idx]} dengan skor {score:.4f}")