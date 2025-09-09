from django.contrib import admin

from .models import Release, Track

class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("branding", "number", "started_at")
    search_fields = ("branding", "number", "description")
    list_filter = ("branding", "started_at")

admin.site.register(Release, ReleaseAdmin)
admin.site.register(Track)
