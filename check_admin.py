import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_project.settings')
django.setup()

from django.contrib.admin import site
from system_modules.models import LandingPageSettings

print('Registered models:')
for model, admin_obj in site._registry.items():
    print(f'  {model._meta.app_label} -> {model.__name__} ({admin_obj.__class__.__name__})')
