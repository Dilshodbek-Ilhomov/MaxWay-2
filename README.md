# 🚀 Maxway — Fast Food Delivery

**Liquid Glass · Apple Vision Pro Style · Bilingual (UZ/EN)**

## O'rnatish / Installation

### 1. Virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Dependencylarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. PostgreSQL database yaratish
```sql
CREATE DATABASE maxway_db;
CREATE USER maxway_admin WITH PASSWORD 'root123';
GRANT ALL PRIVILEGES ON DATABASE maxway_db TO maxway_admin;
```

### 4. Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Server ishga tushirish
```bash
python manage.py runserver
```

## URLs
- **Asosiy sahifa:** `http://localhost:8000/uz/`
- **Inglizcha:** `http://localhost:8000/en/`
- **Admin panel:** `http://localhost:8000/admin/`

## Til o'zgartirish
Navbar'dagi 🇺🇿/🇺🇸 tugmasi orqali til almashtiriladi.

## Texnologiyalar
- Django 6.0.3
- PostgreSQL
- Liquid Glass CSS (custom)
- Django i18n (UZ + EN)
