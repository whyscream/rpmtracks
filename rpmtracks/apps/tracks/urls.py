from django.urls import path

from . import views

app_name = "tracks"
urlpatterns = [
    path("release/<str:release_number>/track/<int:pk>/", views.TrackDetailView.as_view(), name="detail"),
    path("release/<str:release_number>/", views.TrackListView.as_view(), name="list_by_release"),
    path("", views.TrackListView.as_view(), name="list"),
]
