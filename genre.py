import os
import json
import spotipy
import argparse

AUTH_TOKEN="BQC7_a5fFCsolt-IwGz8TdhAQXCXGqmG-SpUpVq-IYjTtubsqvF61OSIUy_dKDOcPUupaAmeEdT0DKSjrsWBpXHEFL1GHQyEz7veZnN-YlRmSU99UJPO8YPQB_ZCHjDM8ZsPJMC36oIJ"

def estimate_artist_genre(artist_name, GENRES_MAP):
    spotify = spotipy.Spotify(auth=AUTH_TOKEN)
    results = spotify.search(q='artist:' + artist_name, type='artist', limit=1)

    genres = []
    for item in results['artists']['items']:
        genres += item['genres']

    if len(genres) == 0:
        return "Unknown", "Unknown"

    # Map spotify genre to our list of main genres
    for main_genre in GENRES_MAP:
        for sub_genre in GENRES_MAP[main_genre]:
            for spotify_genre in genres:
                if sub_genre in spotify_genre.lower():
                    return main_genre.title(), spotify_genre.title()


    return "Unknown", genres[0].title()


if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='download_midi.py')
    parser.add_argument('--midi', type=str, required=True, help="Path to a folder with midi files.")
    parser.add_argument('--genres', type=str, required=True, help="Path to the gender mapping file.")
    opt = parser.parse_args()

    # Load genres mapping
    genre_mapping = None
    with open(opt.genres) as f:
        genre_mapping = json.load(f)

    # Load all files to be added
    for dir, _ , files in os.walk(opt.midi):
        if len(files) == 0:
            continue

        artist_name  = dir.split("/")[-1]

        # Get artist genre from Spotify API
        artist_genre, artist_subgenre = estimate_artist_genre(artist_name, genre_mapping)

        print(artist_name, "-", artist_genre,"-" ,artist_subgenre)
