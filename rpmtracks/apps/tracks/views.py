from django.views.generic import ListView

from .models import Track


class TrackListView(ListView):
    template_name = "tracks/track_list.html"
    context_object_name = "tracks"

    def get_queryset(self):
        latest_release = Track.objects.order_by("-number").first()
        return Track.objects.filter(release=latest_release.release)
