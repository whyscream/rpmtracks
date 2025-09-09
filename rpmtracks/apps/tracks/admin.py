from django.contrib import admin

from .models import Release, Track

class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("branding", "number", "started_at")
    search_fields = ("branding", "number", "description")
    list_filter = ("branding", "started_at")
    ordering = ("number",)

class TrackAdmin(admin.ModelAdmin):
    list_display = ("release", "number", "title", "author", "duration", "workout")
    list_display_links = ("number", "title", "author")
    search_fields = ("title", "author", "cover_artist", "workout", "notes", "release__branding", "release__number")
    list_filter = ("release__branding", "workout", "number")
    ordering = ("-release__number", "number")

admin.site.register(Release, ReleaseAdmin)
admin.site.register(Track, TrackAdmin)
