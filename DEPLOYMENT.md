# 🚀 Deployment Checklist - Nkula WUA Accounting System

## ✅ Pre-Deployment Checklist#

### 1. Environment Setup#
- [ ] Copy `.env.example` to `.env`
- [ ] Generate strong SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up database (PostgreSQL recommended for production)

### 2. Database#
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Load initial data if needed

### 3. Static & Media Files#
- [ ] Run: `python manage.py collectstatic`
- [ ] Configure media storage (local or cloud)
- [ ] Set proper file permissions

### 4. Security#
- [ ] `DEBUG=False`
- [ ] Strong SECRET_KEY set
- [ ] `ALLOWED_HOSTS` configured
- [ ] HTTPS enabled (SSL/TLS)
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`

### 5. Email Configuration#
- [ ] Set `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- [ ] Test email sending

### 6. Web Server#
- [ ] Install Gunicorn: `pip install gunicorn`
- [ ] Test: `gunicorn accounting_project.wsgi:application`
- [ ] Configure with Nginx/Apache

## 🌐 PythonAnywhere Deployment#

1. **Upload Project**
   - Zip project (excluding venv, .git, __pycache__)
   - Upload via PythonAnywhere dashboard

2. **Setup Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   workon myenv
   pip install -r requirements.txt
   ```

3. **Configure Web App**
   - Go to Web tab → Add new web app
   - Choose Manual configuration
   - Select Python 3.10+
   - Set path: `/home/yourusername/djang-project`

4. **WSGI Configuration**
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

5. **Environment Variables**
   - Add to WSGI file or use PythonAnywhere environment variables
   - Set `DJANGO_SETTINGS_MODULE=accounting_project.settings`

6. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

7. **Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

## 🔧 Gunicorn Setup (Alternative)#

```bash
# Install
pip install gunicorn

# Run (test)
gunicorn accounting_project.wsgi:application --bind 0.0.0.0:8000

# Production with workers
gunicorn accounting_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
```

## 📋 Requirements.txt#

Already generated. Key packages:
- Django==5.2.3
- django-crispy-forms
- crispy-bootstrap5
- whitenoise
- python-dotenv
- dj-database-url
- gunicorn (for production)

## ⚠️ Common Issues#

1. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` and `STATIC_URL`
   - Verify WhiteNoise middleware is installed

2. **Database connection error**
   - Check `DATABASE_URL` in `.env`
   - Verify PostgreSQL is running (if using)

3. **Permission denied on media uploads**
   - Set proper permissions: `chmod 755 media/`
   - Check ownership

4. **WebRTC calls not working**
   - Requires HTTPS in production
   - Configure SSL certificate
   - Check browser permissions

## 📞 Support#

- **Email**: nkulawuamw@gmail.com
- **Phone**: +265 982 960 373
- **Location**: Matandika Village, T/A Nkula, Machinga District, Malawi

---

**Developed by Mantchombe Technology**
