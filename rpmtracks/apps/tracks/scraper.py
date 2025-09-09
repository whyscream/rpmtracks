import logging
import re
from datetime import timedelta

import httpx
from bs4 import BeautifulSoup, Tag

from .models import Release, Track

logger = logging.getLogger(__name__)

SOURCE_URL = "https://seesaawiki.jp/tracklist/d/RPM"


def parse_track(row: Tag) -> dict | None:
    """
    Parse track data from a HTML table row.

    Returns a dictionary with track details or None if the track is to be skipped.
    """
    cols = row.find_all("td")
    if cols[0].attrs.get("colspan") or cols[0].attrs.get("rowspan"):
        # This is a image column, discard it
        del cols[0]

    if len(cols) == 6:
        track_id = cols[0].get_text(strip=True)
        track_name = cols[1].get_text(strip=True)
        track_author = cols[2].get_text(strip=True)
        track_cover_artist = cols[3].get_text(strip=True)
        track_duration = cols[4].get_text(strip=True)
        track_workout = cols[5].get_text(strip=True)
    elif len(cols) == 5:
        track_id = cols[0].get_text(strip=True)
        track_name = cols[1].get_text(strip=True)
        track_author = cols[2].get_text(strip=True)
        track_cover_artist = None
        track_duration = cols[3].get_text(strip=True)
        track_workout = cols[4].get_text(strip=True)
    else:
        raise ValueError(f"Unexpected number of columns: {len(cols)}")

    if track_id == "IMAGE":
        # This is a header row, skip it
        return None

    # remove duplicate durations
    if match := re.match(r"(\d+:\d{2})", track_duration):
        track_duration = match.group(1)

    # Extract RPM release from track_id
    branding = None
    release = None
    track_number = None
    # track id RPM or BB + all numerics is a normal track
    if match := re.fullmatch(r"(?P<branding>RPM|BB)(?P<release>\d+)(?P<track_number>\d{2})", track_id):
        branding = match.group("branding")
        release = match.group("release")
        track_number = match.group("track_number")
    # track id RPM + numeric + random string is a bonus track of sorts
    elif match := re.fullmatch(r"(?P<branding>RPM|BB)(?P<release>\d+)(?P<track_number>.*)", track_id):
        branding = match.group("branding")
        release = match.group("release")
        track_number = match.group("track_number")
    elif "RPMUN" in track_id:
        # TODO: No idea what this is, skipping for now
        return None
    else:
        raise ValueError(f"Unexpected track ID: {track_id}")

    track = {
        "id": track_id,
        "branding": branding,
        "release": release,
        "track_number": track_number,
        "name": track_name,
        "author": track_author,
        "cover_artist": track_cover_artist,
        "duration": track_duration,
        "workout": track_workout,
    }
    logger.debug("Track details: %s", track)
    return track

def parse_tracks_from_html(html: str) -> list[dict]:
    """Parse all tracks from the provided HTML content."""
    soup = BeautifulSoup(html, "html.parser")

    tracklists = []
    tracklists.append(soup.find("table", id="content_block_1"))
    tracklists.append(soup.find("table", id="content_block_4"))
    tracklists.append(soup.find("table", id="content_block_7"))
    tracklists.append(soup.find("table", id="content_block_10"))
    tracks = []
    for tracklist in tracklists:
        for row in tracklist.find_all("tr")[1:]:
            track = parse_track(row)
            if track:
                tracks.append(track)
    return tracks

def scrape_tracks() -> list[dict]:
    """Scrape tracks from the SOURCE_URL."""
    response = httpx.get(SOURCE_URL)
    response.raise_for_status()  # Ensure we raise an error for bad responses
    return parse_tracks_from_html(response.text)


def duration_str_to_timedelta(duration_str: str):
    """Convert a duration string (MM:SS) to a timedelta object."""
    minutes, seconds = map(int, duration_str.split(":"))
    return timedelta(minutes=minutes, seconds=seconds)

def import_tracks():
    """Scrape tracks and save them to the database."""
    tracks_data = scrape_tracks()
    for track_data in tracks_data:
        release, _release_created = Release.objects.update_or_create(
            number=int(track_data["release"]),
            branding=track_data["branding"],
        )
        if _release_created:
            logger.info(f"Created new release: {release}")

        # track, _track_created = Track.objects.update_or_create(
        #     number=track_data["track_number"],
        #     release=release,
        #     defaults={
        #         "title": track_data["name"],
        #         "author": track_data["author"],
        #         "cover_artist": track_data["cover_artist"] or "",
        #         "duration": duration_str_to_timedelta(track_data["duration"]),
        #         "notes": f"workout={track_data["workout"]}" if track_data["workout"] else "",
        #     },
        # )
        # if _track_created:
        #     logger.info(f"Created new track: {track} in release {release}")

    return tracks_data

if __name__ == "__main__":
    tracks = scrape_tracks()
    print(tracks)
    print("Total tracks:", len(tracks))
