from django.shortcuts import redirect
from django.views.generic import ListView, RedirectView, DetailView

from .forms import SelectReleaseForm
from .models import Track, Release

class TrackListView(ListView):
    template_name = "tracks/track_list.html"
    context_object_name = "tracks"
    http_method_names = ["get", "post", "head", "options", "trace"]

    release = None
    select_release_form = None

    def get_queryset(self):
        return Track.objects.filter(release=self.release)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx["release"] = self.release
        ctx["next_release"] = Release.objects.filter(number__gt=self.release.number).order_by("number").first()
        ctx["previous_release"] = Release.objects.filter(number__lt=self.release.number).order_by("-number").first()
        ctx["select_release_form"] = self.select_release_form
        return ctx

    def get(self, request, release_number=None, *args, **kwargs):
        if release_number is not None:
            self.release = Release.objects.get(number=release_number)
        else:
            self.release = Release.objects.latest("number")

        self.select_release_form = SelectReleaseForm(initial={"release": self.release})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = SelectReleaseForm(request.POST)
        if form.is_valid():
            return redirect("tracks:list_by_release", release_number=form.cleaned_data["release"].number)

        return self.get(request, *args, **kwargs)


class TrackDetailView(DetailView):
    template_name = "tracks/track_detail.html"
    context_object_name = "track"
    http_method_names = ["get", "head", "options", "trace"]
    model = Track

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["next_track"] = Track.objects.filter(release=self.object.release, number__gt=self.object.number).order_by("number").first()
        ctx["previous_track"] = Track.objects.filter(release=self.object.release, number__lt=self.object.number).order_by("-number").first()
        return ctx
