<<<<<<< HEAD
# Nkula Water Users Association - Accounting Management System

A comprehensive Django-based accounting system for community water management organizations.

## 🌊 Features

- **Beneficiary Management** - Track water users, balances, and payments
- **Invoice & Payment Tracking** - Complete billing system
- **Expense Management** - Monitor organizational expenses
- **Reports & Analytics** - Financial reports with PDF/Excel export
- **User Management** - Role-based access (Admin, Manager, Accountant, Viewer)
- **Year-End Rollover** - Automatic balance carry-forward
- **Internal Chat & Calls** - WebRTC voice/video calling
- **WhatsApp Integration** - Direct messaging support
- **Landing Page** - Customizable public website with gallery
- **Service Management** - Showcase services with images/captions
- **Theme Settings** - Admin-configurable colors and styling

## 📋 Requirements

- Python 3.8+
- Django 5.2.3
- Django Crispy Forms
- WhiteNoise (static file serving)
- python-dotenv
- dj-database-url
- Additional packages in `requirements.txt`

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/djang-project.git
   cd djang-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Production Deployment

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@localhost/dbname
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Deployment Steps

1. **Set DEBUG=False** in `.env`
2. **Configure ALLOWED_HOSTS** with your domain
3. **Use PostgreSQL** (recommended for production):
   ```env
   DATABASE_URL=postgres://user:password@localhost:5432/dbname
   ```
4. **Run with WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn accounting_project.wsgi:application
   ```

### For PythonAnywhere

1. Upload project to PythonAnywhere
2. Set up virtual environment
3. Configure WSGI file:
   ```python
   import os
   import sys
   path = '/home/yourusername/djang-project'
   if path not in sys.path:
       sys.path.append(path)
   os.environ['DJANGO_SETTINGS_MODULE'] = 'accounting_project.settings'
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
4. Set environment variables in WSGI config

## 📁 Project Structure

```
djang-project/
├── account_project/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── account_app/               # Main application
│   ├── models.py              # Database models
│   ├── views.py               # View controllers
│   ├── admin.py              # Admin interface
│   └── templates/            # HTML templates
├── media/                      # User-uploaded files
├── static/                    # Static assets
├── staticfiles/               # Collected static files
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🎨 Customization

### Landing Page Theme

1. Login to `/admin/`
2. Go to **Landing Page Settings**
3. Customize colors:
   - Primary/Secondary colors
   - Hero gradient
   - CTA section colors
   - WhatsApp icon color

### Gallery & Services

- **Gallery Images** - Upload images for gallery section
- **Services** - Add services with images and captions

## 📞 Support

- **Email**: nkulawuamw@gmail.com
- **Phone**: +265 982 960 373
- **Location**: Matandika Village, T/A Nkula, Machinga District, Malawi

## 📄 License

This project is proprietary software owned by Nkula Water Users Association.

---

**Developed by Mantchombe Technology**
=======
# nkula_wua
>>>>>>> 7621ad4e77a91170a6eff3552c315ecd589ea412
