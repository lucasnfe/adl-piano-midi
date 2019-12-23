import os
import json
import argparse

from utils import get_midi_files
from start import add_song
from load import *

# Parse arguments
parser = argparse.ArgumentParser(description='download_midi.py')
parser.add_argument('--adl', type=str, required=True, help="Path to the current dataset.")
parser.add_argument('--new', type=str, required=True, help="Path to the new midi to be added.")
parser.add_argument('--genres', type=str, required=True, help="Path to the genres mapping.")
opt = parser.parse_args()

# Load genres mapping
genre_mapping = None
with open(opt.genres) as f:
    genre_mapping = json.load(f)

# Load adl dataset and songs
adl_dataset = adl_load_dataset(opt.adl)
adl_songs = adl_songs(adl_dataset)

# Load all files to be added
for dir, _ , files in os.walk(opt.new):
    if len(files) == 0:
        continue

    # Get artist genre from Spotify API
    artist_name  = dir.split("/")[-1]

    midi_files = get_midi_files(files)
    for midi_name in midi_files:
        song_path = os.path.join(dir, midi_name)
        # Compute file MD5
        with open(song_path, "rb") as midi_file:
            midi_md5 = hashlib.md5(midi_file.read()).hexdigest()
            song_name = os.path.splitext(midi_name)[0]

            if midi_md5 not in adl_songs:
                print("- Adding song", song_name, "by", artist_name)
                adl_songs[midi_md5] = add_song(song_path, song_name, artist_name, opt.adl, genre_mapping)
            else:
                print("x song already in dataset", song_name, "by", artist_name)
