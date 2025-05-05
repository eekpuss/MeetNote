# Panduan Setup MeetNote

## Daftar Isi
1. [Ringkasan](#ringkasan)
2. [Persyaratan Sistem](#persyaratan-sistem)
3. [Setup Backend](#setup-backend)
4. [Setup Frontend](#setup-frontend)
5. [Menjalankan Aplikasi](#menjalankan-aplikasi)
6. [Troubleshooting](#troubleshooting)

## Ringkasan

MeetNote adalah aplikasi web untuk mencatat notulen meeting dan mengelola todo list. Aplikasi ini menggunakan:
- **Backend**: Python dengan Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, dan JavaScript

## Persyaratan Sistem

Sebelum memulai, pastikan Anda memiliki:

- Python 3.8 atau lebih baru
- Node.js dan npm (untuk pengembangan frontend)
- Git (opsional, untuk manajemen versi)
- pdfkit dan wkhtmltopdf (untuk ekspor PDF)

## Setup Backend

### 1. Clone Repository (opsional)

```bash
git clone https://github.com/yourusername/meetnote.git
cd meetnote
```

### 2. Membuat Virtual Environment

```bash
# Untuk Windows
cd backend
python -m venv venv
venv\Scripts\activate

# Untuk Mac/Linux
cd backend
python -m venv venv
source venv/bin/activate
```

### 3. Menginstal Dependensi

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment

Buat file `.env` di direktori backend:

```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DEBUG=True
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

Catatan: Untuk Gmail, Anda perlu menggunakan "App Password" dan bukan password akun reguler.

### 5. Inisialisasi Database

```bash
mkdir -p database
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

Ini akan membuat file database SQLite di `backend/database/meetnote.db`.

### 6. Menginstal wkhtmltopdf (untuk ekspor PDF)

- **Windows**: Download dan install dari [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)
- **Mac**: `brew install wkhtmltopdf`
- **Linux**: `sudo apt-get install wkhtmltopdf`

## Setup Frontend

### 1. Struktur File

Pastikan struktur folder frontend sudah sesuai dengan rancangan:

```
frontend/
  ├── index.html
  ├── login.html
  ├── assets/
  │   ├── css/
  │   ├── js/
  │   ├── img/
  │   └── fonts/
  ├── components/
  └── pages/
```

### 2. Menginstal Library Frontend (opsional, jika menggunakan npm)

```bash
cd frontend
npm init -y
npm install bootstrap @popperjs/core
```

## Menjalankan Aplikasi

### 1. Menjalankan Backend

```bash
cd backend
source venv/bin/activate  # atau venv\Scripts\activate di Windows
python app.py
```

Server akan berjalan di http://localhost:5000

### 2. Menjalankan Frontend

Untuk pengembangan, Anda dapat menggunakan server sederhana:

```bash
cd frontend
python -m http.server 8000
```

Atau jika Anda menginstal Node.js:

```bash
cd frontend
npx serve
```

Kemudian buka browser dan akses http://localhost:8000

## Troubleshooting

### Masalah Dependensi

Jika muncul konflik dependensi seperti:

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed...
```

Solusi:
1. Gunakan virtual environment terpisah untuk proyek ini.
2. Perbarui versi paket yang berkonflik:
   ```
   pip install Jinja2>=3.0.3
   pip install requests>=2.31.0
   ```

### Masalah PDF Generation

Jika ekspor PDF tidak berfungsi:

1. Pastikan wkhtmltopdf terinstal dan tersedia di PATH sistem.
2. Periksa path wkhtmltopdf di kode atau set secara manual:
   ```python
   config = pdfkit.configuration(wkhtmltopdf='/path/to/wkhtmltopdf')
   pdf = pdfkit.from_string(html_content, False, configuration=config)
   ```

### Masalah Database

Jika ada error terkait database:

1. Pastikan folder `database` sudah dibuat.
2. Jika skema berubah, Anda mungkin perlu menghapus database dan membuatnya kembali:
   ```bash
   rm backend/database/meetnote.db
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

### Masalah CORS

Jika frontend tidak dapat mengakses backend karena masalah CORS:

1. Pastikan Flask-CORS sudah diatur dengan benar di `app.py`.
2. Periksa URL yang Anda gunakan sesuai dengan konfigurasi CORS.