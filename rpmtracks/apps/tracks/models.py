from django.db import models

class Release(models.Model):
    class Branding(models.TextChoices):
        RPM = "RPM", "RPM"
        BB = "BB", "Body Bike",
        OTHER = "OTHER", "Other"

    number = models.IntegerField()
    branding = models.CharField(max_length=32, choices=Branding.choices, default=Branding.RPM)
    description = models.CharField(max_length=255, blank=True)
    started_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.branding} {self.number:02d}"


class Track(models.Model):
    class Workout(models.TextChoices):
        WALK_IN = "Walk in", "Walk in"
        WARMUP = "Warmup", "Warmup"
        MOUNTAIN_CLIMB = "Mountain climb", "Mountain climb"
        SPEED_WORK = "Speed work", "Speed work"
        RIDE_HOME = "Ride home", "Ride home (cool down/stretch)"
        UNKNOWN = "", ""

    number = models.CharField(max_length=32, help_text="Track number within the release, can be non-numeric for bonus tracks")
    release = models.ForeignKey(Release, on_delete=models.CASCADE, related_name="tracks")
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover_artist = models.CharField(max_length=255, blank=True)
    duration = models.DurationField()
    workout = models.CharField(max_length=32, choices=Workout.choices, default=Workout.UNKNOWN)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.release} - {self.number} - {self.title}"
