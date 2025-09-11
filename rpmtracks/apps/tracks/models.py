from django.db import models

class Release(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("number", "branding"), name="release_number_branding"),
        ]

    class Branding(models.TextChoices):
        RPM = "RPM", "RPM"
        BB = "BB", "Body Bike",
        OTHER = "OTHER", "Other"

    number = models.IntegerField()
    branding = models.CharField(max_length=32, choices=Branding.choices, default=Branding.RPM)
    description = models.CharField(max_length=255, blank=True)
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="Timestamp when this record was created")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="Timestamp when this record was last updated")


    def __str__(self):
        return f"{self.branding} {self.number:02d}"


class Track(models.Model):
    class Workout(models.TextChoices):
        WALK_IN = "Walk in", "Walk in"
        WARMUP = "Warmup", "Warmup"
        PACE = "Pace", "Pace"
        HILLS = "Hills", "Hills"
        MIXED_TERRAIN = "Mixed terrain", "Mixed terrain"
        INTERVALS = "Intervals", "Intervals"
        SPEED_WORK = "Speed work", "Speed work"
        FREE_SPIN = "Free spin", "Free spin"
        MOUNTAIN_CLIMB = "Mountain climb", "Mountain climb"
        RIDE_HOME = "Ride home", "Ride home (cool down)"
        UNKNOWN = "Unknown", "Unknown"
        NONE = "", "-"

    number = models.CharField(max_length=32, help_text="Track number within the release, can be non-numeric for bonus tracks")
    release = models.ForeignKey(Release, on_delete=models.CASCADE, related_name="tracks")
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover_artist = models.CharField(max_length=255, blank=True)
    duration = models.DurationField()
    workout = models.CharField(max_length=32, choices=Workout.choices, default=Workout.UNKNOWN, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="Timestamp when this record was created")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="Timestamp when this record was last updated")

    def __str__(self):
        return f"{self.release} - {self.number} - {self.title}"
