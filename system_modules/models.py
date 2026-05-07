from django.db import models
from accounting_app.models import LandingPageSettings as OriginalLandingPageSettings


class LandingPageSettings(OriginalLandingPageSettings):
    """Proxy model to display LandingPageSettings under System Modules in admin."""

    class Meta:
        proxy = True
        app_label = "system_modules"
        verbose_name = "Landing Page Settings"
        verbose_name_plural = "Landing Page Settings"
