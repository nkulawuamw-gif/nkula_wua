# PythonAnywhere Deployment Guide

## Prerequisites
- PythonAnywhere account (Free tier works)
- Git repository pushed to GitHub/GitLab

## Step 1: Create Web App
1. Log in to https://www.pythonanywhere.com
2. Go to **Web** tab → **Add a new web app**
3. Select **Manual configuration** → **Python 3.10** (or latest available)
4. Note your username from the URL: `https://www.pythonanywhere.com/user/<YOUR_USERNAME>/`

## Step 2: Clone Repository
1. Open a **Bash console** on PythonAnywhere
2. Clone your repository:
   ```bash
   cd ~
   git clone <your-repo-url> "djang project"
   cd "djang project"
   ```

## Step 3: Setup Virtual Environment
```bash
cd ~/djang\ project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables
1. Create `.env` file in project root:
   ```bash
   nano .env
   ```
2. Add your production values (see `.env.example` for reference):
   ```
   SECRET_KEY=<generate-a-new-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=<YOUR_USERNAME>.pythonanywhere.com
   DATABASE_URL=sqlite:///db.sqlite3
   ```
3. Generate a secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

## Step 5: Configure WSGI
1. Go to **Web** tab → Click on your web app
2. Scroll to **Code** section → Click the WSGI configuration file link
3. Replace ALL contents with `wsgi_pythonanywhere.py`
4. Update `<YOUR_USERNAME>` with your actual username
5. Save the file

## Step 6: Configure Static & Media Files
In the **Web** tab, under **Static files**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/<YOUR_USERNAME>/djang project/staticfiles/` |
| `/media/` | `/home/<YOUR_USERNAME>/djang project/media/` |

## Step 7: Run Migrations & Collect Static
In Bash console:
```bash
cd ~/djang\ project
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Step 8: Reload Web App
1. Go to **Web** tab
2. Click the green **Reload** button
3. Visit `https://<YOUR_USERNAME>.pythonanywhere.com`

## Updating the App
When you push new code:
```bash
cd ~/djang\ project
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```
Then reload the web app from the **Web** tab.

## Notes
- **Free tier**: SQLite only, 512MB storage, app sleeps after inactivity
- **Paid tiers**: PostgreSQL support, always-on, more resources
- **Logs**: Check **Web** tab → Error log / Server log for debugging
- **Database**: If migrating from local SQLite, upload `db.sqlite3` to project root
