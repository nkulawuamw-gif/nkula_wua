# 🌐 Wesmmer Deployment Guide - Nkula WUA Accounting System#

## Prerequisites#

1. **Wesmmer account** - Sign up at https://wesmmer.com
2. **Wesmmer CLI installed** (optional, you can use dashboard)
3. **GitHub repository** with your project code#

## 📦 Step-by-Step Deployment#

### 1. Prepare Project for Wesmmer#

✅ **Already done:**
- `requirements.txt` - All dependencies listed
- `wesphere.toml` - Wesmmer configuration
- `runtime.txt` - Python version (create if needed)
- Static files configured with WhiteNoise
- Environment variables ready#

### 2. Create GitHub Repository#

```bash
# If git not installed, download from https://git-scm.com
cd "E:\Websites projects\djang project"
git init
git add .
git commit -m "Initial commit: Production-ready Django accounting system"
```

Create repo on GitHub.com, then:
```bash
git remote add origin https://github.com/yourusername/nkula-wua-accounting.git
git push -u origin master
```

### 3. Deploy to Wesmmer#

#### Option A: Using Wesmmer Dashboard (Easiest)#

1. **Login to Wesmmer** - https://wesmmer.com/dashboard
2. **Create New App:**
   - Click "Create App"
   - Choose "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select `nkula-wua-accounting` repository
   - Choose region (closest to Malawi: `Europe` or `US`)

3. **Configure Environment:**
   - Go to app settings
   - Add environment variables:
     ```
     DJANGO_SETTINGS_MODULE=accounting_project.settings
     DEBUG=False
     SECRET_KEY=your-very-secret-key-generate-with-python
     ALLOWED_HOSTS=nkula-wua-accounting.wesphere.app
     DATABASE_URL=sqlite:///db.sqlite3
     EMAIL_HOST_USER=nkulawuamw@gmail.com
     EMAIL_HOST_PASSWORD=your-app-password
     EMAIL_PORT=587
     ```

4. **Deploy:**
   - Wesmmer will automatically detect `wesphere.toml`
   - Build and deployment starts automatically
   - Wait for deployment to complete (5-10 minutes)

#### Option B: Using Wesmmer CLI#

```bash
# Install Wesmmer CLI (if not installed)
pip install wesphere

# Login
wesphere login

# Create app
wesphere apps create nkula-wua-accounting --region us-west

# Set environment variables
wesphere config:set DJANGO_SETTINGS_MODULE=accounting_project.settings
wesphere config:set DEBUG=False
wesphere config:set SECRET_KEY=your-secret-key
wesphere config:set ALLOWED_HOSTS=nkula-wua-accounting.wesphere.app

# Deploy
git push wesphere master
```

### 4. Post-Deployment Setup#

1. **Run Migrations:**
   ```bash
   wesphere run python manage.py migrate
   ```

2. **Create Superuser:**
   ```bash
   wesphere run python manage.py createsuperuser
   ```

3. **Verify Deployment:**
   - Visit: `https://nkula-wua-accounting.wesphere.app`
   - Test login at: `https://nkula-wua-accounting.wesphere.app/login/`
   - Check admin at: `https://nkula-wua-accounting.wesphere.app/admin/`

## 🔧 Important Wesmmer Commands#

```bash
# Check logs
wesphere logs --tail=100

# Run management commands
wesphere run python manage.py <command>

# Restart app
wesphere restart

# Check app info
wesphere apps:info nkula-wua-accounting

# Scale workers (if needed)
wesphere scale web=2
```

## 📋 Environment Variables for Wesmmer#

Copy to Wesmmer dashboard → Settings → Environment Variables:

```env
DJANGO_SETTINGS_MODULE=accounting_project.settings
DEBUG=False
SECRET_KEY=your-very-secret-key-generate-with-python
ALLOWED_HOSTS=nkula-wua-accounting.wesphere.app,localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_USER=nkulawuamw@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🎯 Custom Domain (Optional)#

1. Go to Wesmmer dashboard → Domains
2. Add your domain: `www.nkulawua.org`
3. Update DNS:
   ```
   CNAME: nkula-wua-accounting.wesphere.app
   ```
4. Enable HTTPS (automatic with Wesmmer)

## ⚠️ Common Issues#

### 1. **Static files not loading**
```bash
wesphere run python manage.py collectstatic --noinput
wesphere restart
```

### 2. **Database connection error**
- Check `DATABASE_URL` in environment variables
- For SQLite: `sqlite:///db.sqlite3`
- For PostgreSQL: `postgres://user:pass@host:5432/dbname`

### 3. **Application error**
```bash
wesphere logs --tail=50
# Check for missing environment variables or migration issues
```

### 4. **Media uploads not working**
- Wesmmer Ephemeral filesystem - files uploaded to media/ may be lost on restart
- **Solution:** Use cloud storage (AWS S3, Google Cloud Storage)
- Or use SQLite for simplicity (small files)

## 🚀 Quick Checklist#

- [ ] GitHub repo created and code pushed
- [ ] Wesmmer app created
- [ ] Environment variables set
- [ ] First deployment successful
- [ ] Migrations run
- [ ] Superuser created
- [ ] Site accessible at `.wesphere.app`
- [ ] SSL/HTTPS working (automatic)
- [ ] Static files loading
- [ ] Media uploads working (or configured cloud storage)

## 📞 Support#

- **Wesmmer Docs:** https://docs.wesphere.com
- **Wesmmer Support:** https://wesmmer.com/support
- **Nkula WUA Email:** nkulawuamw@gmail.com
- **Developer:** Mantchombe Technology

---

**🎉 Your Django app will be live at:**
`https://nkula-wua-accounting.wesphere.app`

**Developed by Mantchombe Technology**
