# 💰 Inventaris — Django Inventaris App

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.14+-blue?logo=python" alt="Python 3.14.0"></a>
  <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/Django-5.x-green?logo=django" alt="Django 6.0.1"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql" alt="PostgreSQL"></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-orange" alt="License MIT"></a>
</p>

<!-- ---

## 🧭 Overview

**Finance** adalah aplikasi berbasis **Django** untuk membantu pengguna mencatat, memantau, dan menganalisis keuangan bulanan dengan efisien.  
Project ini menggunakan **PostgreSQL** sebagai basis data utama dan menyimpan konfigurasi sensitif di file `.env`.

---

## ⚙️ Features
- ✨ Multi-user financial tracking  
- 📊 Income & expense categorization  
- 📅 Monthly summary dashboard  
- 🔐 Environment-based configuration  
- 🗄 PostgreSQL database support  

--- -->

## 🧱 Tech Stack
| Layer | Technology |
|-------|-------------|
| Backend | Django 6.x |
| Database | PostgreSQL 15+ |
| Language | Python 3.14+ |

---

## 🚀 Getting Started

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/inventaris.git
cd inventaris
```

### 2️⃣ Setup Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Buat file `.env` di root folder:
```env
SECRET_KEY=django-insecure-your-secret-key
DEBUG=True

DB_NAME=inventaris_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 5️⃣ Apply Migrations
```bash
python manage.py migrate
```

### 6️⃣ Run the App
```bash
python manage.py runserver
```

🌐 Buka di browser:  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

<!-- ---

## 🧠 Development Notes
- Semua konfigurasi rahasia disimpan di `.env`  
- Gunakan `venv` agar environment tetap terisolasi  
- Jangan commit file `.env` atau `venv/` ke GitHub  

Tambahkan ke `.gitignore`:
```
venv/
__pycache__/
.env
```

---

## 📦 Requirements
```
Django>=5.0,<6.0
python-dotenv>=1.0.0
psycopg2-binary>=2.9
```

--- -->

## 🧾 License
Distributed under the MIT License.  
Lihat file `LICENSE` untuk detailnya.

---

## 👨‍💻 Author
**Hisyam (MH)**  
📍 Data & Tech Enthusiast  
🌐 [LinkedIn](https://www.linkedin.com) • [GitHub](https://github.com)

---

<p align="center">
  Made with ❤️ using <b>Django + PostgreSQL</b><br>
  <i>"Manage your money like a pro — one transaction at a time."</i>
</p>