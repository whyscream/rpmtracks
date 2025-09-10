from django.urls import path

from . import views

app_name = "tracks"
urlpatterns = [
    path("release/<int:release_number>/", views.TrackListView.as_view(), name="list_by_release"),
    path("", views.TrackListView.as_view(), name="list"),
]
