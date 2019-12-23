import os
import shutil
import spotipy
import argparse

from genre import *

# Parse arguments
parser = argparse.ArgumentParser(description='artist.py')
parser.add_argument('--midi', type=str, required=True, help="Path to a folder with midi files.")
parser.add_argument('--genres', type=str, required=True, help="Path to the genres mapping.")
parser.add_argument('--out', type=str, required=True, help="Path to the output dir.")
opt = parser.parse_args()

spotify = spotipy.Spotify(auth=AUTH_TOKEN)

# Load genres mapping
genre_mapping = None
with open(opt.genres) as f:
    genre_mapping = json.load(f)

for song in os.listdir(opt.midi):
    if os.path.isfile(os.path.join(opt.midi, song)):
         song_name, ext = os.path.splitext(song)

         print(song_name)
         results = spotify.search(q='track:' + song_name, type="track", limit=10)

         for item in results["tracks"]["items"]:
             for artist in item["album"]["artists"]:
                 artist_name = artist["name"]

                 genre, subgenre = estimate_artist_genre(artist_name, genre_mapping)

                 if genre == "Jazz":
                    artist_dir = os.path.join(opt.out, artist_name)
                    
                    # Create artist directory
                    try:
                         os.mkdir(artist_dir)
                    except:
                         print("Artist directory already exists.")

                    song_new_path = os.path.join(artist_dir, song_name + ext)
                    shutil.copyfile(os.path.join(opt.midi, song), song_new_path)
