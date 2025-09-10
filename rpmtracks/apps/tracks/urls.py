from django.urls import path

from . import views

app_name = "tracks"
urlpatterns = [
    path("", views.TrackListView.as_view(), name="list"),
]
