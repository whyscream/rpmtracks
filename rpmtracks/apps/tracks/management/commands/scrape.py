from django.core.management import BaseCommand

from apps.tracks.scraper import scrape_tracks


class Command(BaseCommand):
    help = "Scrape RPM and BB track data from the web"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting the scraping process..."))
        tracks = scrape_tracks()
        releases = []
        for track in tracks:
            if track and track["release"] not in releases:
                releases.append(track["release"])
        self.stdout.write(f"Found {len(releases)} releases and {len(tracks)} tracks.")
        self.stdout.write(self.style.SUCCESS("Scraping completed successfully."))
