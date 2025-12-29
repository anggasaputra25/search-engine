# -----------------------
# ADI - START
# -----------------------
# Import module bawaan Python dan library yang dibutuhkan
import os
import nltk
import pdfplumber
from flask import Flask, render_template, request
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from flask import send_from_directory # Untuk download file PDF

# ===================================================
# SETUP & KONFIGURASI
# ===================================================

app = Flask(__name__) # Inisialisasi aplikasi Flask

# Install NLTK stopwords dan tokenizer jika belum ada
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Stopwords Indonesia
stop_words = set(stopwords.words('indonesian'))

# Sastrawi stemmer
factory = StemmerFactory() # Buat factory stemmer Sastrawi
stemmer = factory.create_stemmer() # Buat objek stemmer

# Folder menyimpan file PDF
folder_path = "documents"
# -----------------------
# ADI - END
# -----------------------

# -----------------------
# DALIANT - START
# -----------------------
# ===============================================
# FUNGSI-FUNGSI
# ===================================================

# Fungsi membaca file PDF
def read_pdf(file_path):
    """Membaca seluruh teks dari file PDF"""
    text = "" # Variabel untuk menampung teks hasil ekstraksi
    try:
        with pdfplumber.open(file_path) as pdf: # Buka PDF
            for page in pdf.pages: # Loop setiap halaman
                text += page.extract_text() + "\n" # Ambil teks dan gabungkan
        return text
    except Exception as e:
        return "" # Jika error, kembalikan teks kosong

# Fungsi preprocessing teks
def preprocess(text):
    """Preprocessing: lowercase, tokenization, stopword removal, stemming"""
    text = text.lower() # Fungsi preprocessing teks
    tokens = nltk.word_tokenize(text) # Tokenisasi teks
    tokens = [t for t in tokens if t not in stop_words] # Hilangkan stopwords
    stemmed = [stemmer.stem(t) for t in tokens] # Lakukan stemming
    return " ".join(stemmed) # Kembalikan sebagai teks lagi
# -----------------------
# DALIANT - END
# -----------------------

# -----------------------
# PANJI
# -----------------------
# Fungsi load semua file PDF dalam folder
def load_documents():
    """Load semua dokumen PDF"""
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')] # List semua PDF
    
    docs = [] # Untuk simpan isi dokumen
    doc_names = [] # Untuk simpan nama file
    
    for pdf_file in pdf_files: # Loop setiap file PDF
        file_path = os.path.join(folder_path, pdf_file) # Gabungkan path folder + nama file
        content = read_pdf(file_path) # Baca isi PDF
        if content: # Jika berhasil dibaca
            docs.append(content)
            doc_names.append(pdf_file)
    
    return docs, doc_names # Kembalikan list dokumen & nama file
# -----------------------
# PANJI - END
# -----------------------

# -----------------------
# SEYA
# -----------------------
# Fungsi pencarian menggunakan TF-IDF + Cosine Similarity
def search_documents(query, docs, doc_names):
    """Melakukan pencarian dengan TF-IDF dan Cosine Similarity"""
    if not docs or not query: # Jika query kosong atau tidak ada dokumen
        return []
    
    # Preprocess
    processed_docs = [preprocess(d) for d in docs] # Preprocessing dokumen
    processed_query = preprocess(query) # Preprocessing query
    
    # TF-IDF
    vectorizer = TfidfVectorizer() # Buat model TF-IDF
    tfidf_matrix = vectorizer.fit_transform(processed_docs + [processed_query]) # TF-IDF: gabungkan semua dokumen + query
    
    doc_vectors = tfidf_matrix[:-1] # Semua dokumen
    query_vector = tfidf_matrix[-1] # Vektor query
    
    # Cosine Similarity
    scores = cosine_similarity(query_vector, doc_vectors)[0] # Hitung kesamaan
    
    # Ranking
    results = [] # List judul + skor yang hasilnya cocok
    for idx, score in enumerate(scores):
        # Filter hanya hasil dengan skor > 0
        if score > 0:
            results.append({
                'name': doc_names[idx], # Nama file
                'score': score, # Nilai cosine similarity
                'score_percent': score * 100, # Versi persen
                'content': docs[idx][:300] # Preview konten dokumen
            })
    
    results.sort(key=lambda x: x['score'], reverse=True) # Urutkan dari skor terbesar
    return results # Kembalikan hasil pencarian
# -----------------------
# SEYA - END
# -----------------------

# -----------------------
# ANGGA - START
# -----------------------
# ===================================================
# ROUTES
# ===================================================

@app.route('/')
def index():
    """Halaman utama"""
    docs, doc_names = load_documents() # Ambil seluruh dokumen PDF dari folder
    return render_template('index.html', 
        total_docs=len(docs), # Kirim jumlah dokumen ke tampilan
        doc_names=doc_names # Kirim nama file untuk ditampilkan pada list
    )

@app.route('/search', methods=['GET' ,'POST'])
def search():
    """Endpoint pencarian"""
    # Ambil kata kunci pencarian dari form (POST) atau URL (GET)
    if request.method == 'POST':
        query = request.form.get('query', '') # Dari form input
    else:
        query = request.args.get('query', '') # Dari parameter URL
    
    # Load dokumen PDF
    docs, doc_names = load_documents()
    # Jalankan fungsi pencarian TF-IDF + Cosine Similarity
    results = search_documents(query, docs, doc_names)

    # Render hasil pencarian kembali ke halaman index
    return render_template('index.html', 
                        query=query, # Tampilkan kembali kata kunci yang dicari
                        results=results, # Hasil pencarian berupa daftar file yang mirip
                        total_docs=len(docs),
                        doc_names=doc_names)

@app.route('/download/<filename>')
def download_file(filename):
    """Route untuk download PDF"""
    return send_from_directory(folder_path, # Lokasi folder PDF
    filename, # Nama file yang akan di-download / dibuka
    as_attachment=False # False = langsung tampil di browser, bukan download otomatis
    )

# Menjalankan server Flask saat file dijalankan langsung (bukan diimport)
if __name__ == '__main__':
    app.run(debug=True) # Mode debug untuk pengembangan (menampilkan error detail)
# -----------------------
# ANGGA - START
# -----------------------