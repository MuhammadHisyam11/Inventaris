# 💰 Inventaris — Django Inventaris App

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.14+-blue?logo=python" alt="Python 3.14.0"></a>
  <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/Django-5.x-green?logo=django" alt="Django 6.0.1"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql" alt="PostgreSQL"></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-orange" alt="License MIT"></a>
</p>

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
git clone https://github.com/<your-username>/Inventaris.git
cd Inventaris
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
Buat file `.env`:
```env
SECRET_KEY=django-insecure-your-secret-key
DEBUG=True

DB_NAME=inventaris_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 5️⃣ Generate Secret Key
Ikuti langkah ini:
```bash
pip install python-dotenv
```

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy hasilnya di terminal dan masukkan ke file `.env`

### 6️⃣ Apply Migrations
```bash
python manage.py migrate
```

### 7️⃣ Run the App
```bash
python manage.py runserver
```

🌐 Buka di browser:  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 🧾 License
Distributed under the MIT License.  
Lihat file `LICENSE` untuk detailnya.

---

## 👨‍💻 Author
**Hisyam (MH)**  
📍 Data & Tech Enthusiast  
🌐 [LinkedIn](https://www.linkedin.com/in/muhammad-hisyam-8a66711b0/) • [GitHub](https://github.com/MuhammadHisyam11)

---

<p align="center">
  Made with ❤️ using <b>Django + PostgreSQL</b><br>
  <i>"Inventaris"</i>
</p>