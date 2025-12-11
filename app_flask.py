import os
import nltk
import pdfplumber
from flask import Flask, render_template, request
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from flask import send_from_directory

# ===================================================
# SETUP & KONFIGURASI
# ===================================================

app = Flask(__name__)

# Install NLTK stopwords
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Stopwords Indonesia
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
        return ""

def preprocess(text):
    """Preprocessing: lowercase, tokenization, stopword removal, stemming"""
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]
    stemmed = [stemmer.stem(t) for t in tokens]
    return " ".join(stemmed)

def load_documents():
    """Load semua dokumen PDF"""
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    docs = []
    doc_names = []
    
    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        content = read_pdf(file_path)
        if content:
            docs.append(content)
            doc_names.append(pdf_file)
    
    return docs, doc_names

def search_documents(query, docs, doc_names):
    """Melakukan pencarian dengan TF-IDF dan Cosine Similarity"""
    if not docs or not query:
        return []
    
    # Preprocess
    processed_docs = [preprocess(d) for d in docs]
    processed_query = preprocess(query)
    
    # TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_docs + [processed_query])
    
    doc_vectors = tfidf_matrix[:-1]
    query_vector = tfidf_matrix[-1]
    
    # Cosine Similarity
    scores = cosine_similarity(query_vector, doc_vectors)[0]
    
    # Ranking
    results = []
    for idx, score in enumerate(scores):
        # Filter hanya hasil dengan skor > 0
        if score > 0:
            results.append({
                'name': doc_names[idx],
                'score': score,
                'score_percent': score * 100,
                'content': docs[idx][:300]
            })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

# ===================================================
# ROUTES
# ===================================================

@app.route('/')
def index():
    """Halaman utama"""
    docs, doc_names = load_documents()
    return render_template('index.html', total_docs=len(docs), doc_names=doc_names)

@app.route('/search', methods=['POST'])
def search():
    """Endpoint pencarian"""
    query = request.form.get('query', '')
    
    docs, doc_names = load_documents()
    results = search_documents(query, docs, doc_names)
    
    return render_template('index.html', 
                        query=query, 
                        results=results, 
                        total_docs=len(docs),
                        doc_names=doc_names)

@app.route('/download/<filename>')
def download_file(filename):
    """Route untuk download PDF"""
    return send_from_directory(folder_path, filename, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)