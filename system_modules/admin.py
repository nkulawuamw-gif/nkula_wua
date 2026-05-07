from django.contrib import admin
from .models import LandingPageSettings


class LandingPageSettingsAdmin(admin.ModelAdmin):
    """Admin for LandingPageSettings under System Modules."""
    list_display = ["primary_color", "is_active", "updated_at"]
    list_filter = ["is_active"]
    fieldsets = (
        ("General", {
            "fields": ("site_name", "hero_title", "hero_subtitle", "hero_description", "is_active")
        }),
        ("About Section", {
            "fields": ("about_title", "about_subtitle", "about_content")
        }),
        ("Vision, Mission & Values", {
            "fields": ("vision_title", "vision_subtitle", "vision_text", "mission_text", "values_text")
        }),
        ("Water Sources Section", {
            "fields": ("water_sources_title", "water_sources_subtitle", "water_sources_images")
        }),
        ("Schemes Section", {
            "fields": ("schemes_title", "schemes_subtitle", "schemes_list")
        }),
        ("Villages Section", {
            "fields": ("villages_title", "villages_subtitle", "villages_list")
        }),
        ("News Section", {
            "fields": ("news_title", "news_subtitle", "news_intro")
        }),
        ("Meetings Section", {
            "fields": ("meetings_title", "meetings_subtitle", "meeting_objectives")
        }),
        ("Projects Section", {
            "fields": ("projects_title", "projects_subtitle", "projects_intro")
        }),
        ("Location Section", {
            "fields": ("location_title", "location_subtitle", "location_address", "location_description")
        }),
        ("Services Section", {
            "fields": ("services_title", "services_subtitle")
        }),
        ("CTA Section", {
            "fields": ("cta_title", "cta_description", "cta_button_text", "cta_gradient_start", "cta_gradient_end")
        }),
        ("Footer", {
            "fields": ("footer_text",)
        }),
        ("Appearance", {
            "fields": ("primary_color", "secondary_color", "text_primary", "text_secondary", "section_bg_light", "section_bg_white")
        }),
    )

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role in ('admin', 'manager')
        return False


admin.site.register(LandingPageSettings, LandingPageSettingsAdmin)
