import re

import httpx
from bs4 import BeautifulSoup

SOURCE_URL = "https://seesaawiki.jp/tracklist/d/RPM"


def parse_track(row):
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

    # remove duplicate durations
    if match := re.match(r"(\d+:\d{2})", track_duration):
        track_duration = match.group(1)

    # Extract RPM release from track_id
    release = None
    track_number = None
    # track id RPM or BB + all numerics is a normal track
    if match := re.match(r"(?:RPM|BB)(?P<release>\d+)(?P<track_number>\d{2})", track_id):
        release = match.group("release")
        track_number = match.group("track_number")
    # track id RPM + numeric + random string is a bonus track of sorts
    elif match := re.match(r"(?:RPM|BB)(?P<release>\d+)(?P<track_number>.*)", track_id):
        release = match.group("release")
        track_number = match.group("track_number")
    elif "RPMUN" in track_id:
        # No idea what this is, skipping for now
        return None

    track = {
        "id": track_id,
        "release": release,
        "track_number": track_number,
        "name": track_name,
        "author": track_author,
        "cover_artist": track_cover_artist,
        "duration": track_duration,
        "workout": track_workout,
    }
    print(track)
    return track


def main():
    # Request the URL
    response = httpx.get(SOURCE_URL)
    # Find the tracklist in the HTML source using beautifulsoup
    soup = BeautifulSoup(response.text, "html.parser")

    tracklists = []
    tracklists.append(soup.find("table", id="content_block_1"))
    tracklists.append(soup.find("table", id="content_block_4"))
    tracklists.append(soup.find("table", id="content_block_7"))
    tracklists.append(soup.find("table", id="content_block_10"))
    # Extract the track data from the tracklists
    tracks = []
    workouts = []
    for tracklist in tracklists:
        for row in tracklist.find_all("tr")[1:]:
            track = parse_track(row)
            tracks.append(track)
            if track and track["workout"] not in workouts:
                workouts.append(track["workout"])

    print(f"Total tracks: {len(tracks)}")
    print(f"Unique workouts: {workouts}")


if __name__ == "__main__":
    main()
