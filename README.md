# 🔍 Search Engine

Search engine berbasis Information Retrieval menggunakan Python dengan implementasi **TF-IDF** dan **Cosine Similarity** untuk pencarian dokumen PDF berbahasa Indonesia.

## 📋 Deskripsi

Aplikasi web ini memungkinkan pengguna untuk melakukan pencarian dokumen PDF berdasarkan kata kunci. Sistem menggunakan metode Information Retrieval dengan preprocessing teks (tokenization, stopword removal, stemming), TF-IDF vectorization, dan Cosine Similarity untuk menghitung relevansi dokumen.

## ✨ Fitur

- 🔎 Pencarian dokumen PDF berdasarkan query
- 📊 Ranking dokumen berdasarkan skor relevansi
- 📄 Preview konten dokumen
- 🇮🇩 Support preprocessing teks Bahasa Indonesia
- 💻 Web interface yang user-friendly
- 📈 Progress bar visual untuk skor relevansi

## 🛠️ Teknologi

- **Python 3.x**
- **Flask** - Web framework
- **NLTK** - Natural Language Toolkit
- **Sastrawi** - Indonesian Stemmer
- **scikit-learn** - TF-IDF & Cosine Similarity
- **pdfplumber** - PDF text extraction

## 📦 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/username/search-engine-pdf.git
cd search-engine-pdf
```

### 2. Install Dependencies

```bash
pip install flask
pip install nltk
pip install Sastrawi
pip install scikit-learn
pip install pdfplumber
```

Atau install semua sekaligus dengan:

```bash
pip install -r requirements.txt
```

### 3. Download NLTK Data

Jalankan Python dan download data yang diperlukan:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

Atau data akan otomatis terdownload saat pertama kali menjalankan aplikasi.

## 📁 Struktur Folder

```
search-engine-pdf/
├── app_flask.py          # Main application
├── templates/
│   └── index.html        # HTML template
├── documents/            # Folder untuk menyimpan PDF
│   ├── dokumen1.pdf
│   └── dokumen2.pdf
├── requirements.txt      # Dependencies
└── README.md
```

## 🚀 Cara Menjalankan

### 1. Masukkan File PDF

Letakkan file PDF yang ingin dicari ke dalam folder `documents/`

```bash
mkdir documents
# Copy file PDF ke folder documents/
```

### 2. Jalankan Aplikasi

```bash
python app_flask.py
```

### 3. Buka Browser

Akses aplikasi di browser:

```
http://localhost:5000
```

### 4. Mulai Pencarian

- Masukkan kata kunci di search box
- Klik tombol **"Cari"**
- Lihat hasil ranking dokumen berdasarkan relevansi

## 📝 Cara Kerja

### 1. **Preprocessing**
   - **Lowercase**: Mengubah semua teks menjadi huruf kecil
   - **Tokenization**: Memecah teks menjadi array kata
   - **Stopword Removal**: Menghapus kata yang tidak bermakna (yang, dan, di, dll)
   - **Stemming**: Mengubah kata ke bentuk dasar (berlari → lari)

### 2. **TF-IDF (Term Frequency-Inverse Document Frequency)**
   - Menghitung bobot kata dalam dokumen
   - Kata yang sering muncul di banyak dokumen diberi bobot lebih rendah
   - Kata yang jarang tapi spesifik diberi bobot lebih tinggi

### 3. **Cosine Similarity**
   - Mengukur kemiripan antara query dan dokumen
   - Skor 0 = tidak relevan
   - Skor 1 = sangat relevan

### 4. **Ranking**
   - Dokumen diurutkan berdasarkan skor tertinggi ke terendah

## 🎯 Contoh Penggunaan

**Query:** `mahasiswa universitas primakara`

**Output:**
```
1. dokumen1.pdf - 85.32%
   Preview: "Saya adalah mahasiswa dari universitas primakara..."

2. dokumen2.pdf - 42.15%
   Preview: "Primakara merupakan kampus yang berada di..."
```

## 📚 Requirements

Buat file `requirements.txt`:

```txt
Flask==3.0.0
nltk==3.8.1
Sastrawi==1.2.0
scikit-learn==1.3.2
pdfplumber==0.10.3
```

## 🐛 Troubleshooting

### Error: Folder 'documents' tidak ditemukan
```bash
mkdir documents
```

### Error: NLTK data tidak ditemukan
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Error: File PDF tidak terbaca
- Pastikan file PDF tidak terenkripsi
- Pastikan file PDF mengandung teks (bukan hasil scan/gambar)

## 🤝 Kontribusi

Kontribusi selalu diterima! Silakan buat pull request atau issue untuk saran dan perbaikan.

## 📄 Lisensi

MIT License - bebas digunakan untuk keperluan apapun.

## 👨‍💻 Author

Dibuat sebagai tugas kampus untuk mata kuliah Information Retrieval.

## 🙏 Acknowledgments

- NLTK untuk Natural Language Processing
- Sastrawi untuk Indonesian Stemmer
- scikit-learn untuk Machine Learning algorithms
- Flask untuk web framework

---

⭐ **Jangan lupa berikan bintang jika project ini membantu!** ⭐