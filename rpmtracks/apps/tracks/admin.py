from django.contrib import admin

from .models import Release, Track

class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("branding", "number", "release_date")
    list_display_links = ("branding", "number", "release_date")
    search_fields = ("branding", "number", "description")
    list_filter = ("branding", "release_date")
    ordering = ("number",)
    readonly_fields = ("created_at", "updated_at")

class TrackAdmin(admin.ModelAdmin):
    list_display = ("release", "number", "title", "author", "duration", "workout")
    list_display_links = ("number", "title", "author")
    search_fields = ("title", "author", "cover_artist", "workout", "remarks", "release__branding", "release__number")
    list_filter = ("release__branding", "workout", "number")
    ordering = ("-release__number", "number")
    readonly_fields = ("created_at", "updated_at")

admin.site.register(Release, ReleaseAdmin)
admin.site.register(Track, TrackAdmin)
