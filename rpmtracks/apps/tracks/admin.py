from django.contrib import admin

from .models import Release, Track

admin.site.register(Track)
admin.site.register(Release)
