# PythonAnywhere WSGI Configuration File
# 
# Instructions:
# 1. Go to https://www.pythonanywhere.com/user/<your-username>/webapps/
# 2. Click on your web app (or create a new one)
# 3. Scroll to the "Code" section and click on the WSGI configuration file link
# 4. Replace the entire contents of that file with this configuration
# 5. Update the paths marked with <YOUR_USERNAME>
# 6. Save and reload the web app

import os
import sys

# -----------------------------------------------------------------------------
# PATH CONFIGURATION - UPDATE THESE
# -----------------------------------------------------------------------------
# Replace <YOUR_USERNAME> with your actual PythonAnywhere username
username = '<YOUR_USERNAME>'
project_name = 'djang project'

# Path to your project directory
path = f'/home/{username}/{project_name}'
if path not in sys.path:
    sys.path.append(path)

# -----------------------------------------------------------------------------
# DJANGO SETTINGS
# -----------------------------------------------------------------------------
os.environ['DJANGO_SETTINGS_MODULE'] = 'accounting_project.settings'

# -----------------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# -----------------------------------------------------------------------------
# Load environment variables from .env file
from dotenv import load_dotenv
env_path = os.path.join(path, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# -----------------------------------------------------------------------------
# WSGI APPLICATION
# -----------------------------------------------------------------------------
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
