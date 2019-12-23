import os
import argparse
import shutil
import json
import hashlib

import million_song as ms

from genre import estimate_artist_genre
from utils import clean_name
from metrics import unique_notes_ratio

def load_song_info_database(datapath):
    songs_info = {}

    for dir_name, sub_dirs, files in os.walk(datapath):
        for file_name in files:
            song_md5 = os.path.splitext(file_name)[0]
            if song_md5 in songs_info:
                raise Exception('MD5 file is duplicated.')

            songs_info[song_md5] = os.path.join(dir_name, file_name)

    return songs_info

def get_version_with_highest_unr(dir_name, versions):
    unrs = {}
    for song_version in versions:
        song_path = os.path.join(dir_name, song_version)
        unrs[song_path] = unique_notes_ratio(song_path)

    return max(unrs, key=unrs.get)

def add_song(song, song_name, artist_name, out_dir="", genre_mapping=None):
    # Estimate artist genre
    genre_dir = out_dir

    if genre_mapping:
        # Get artist genre from Spotify API
        artist_genre, artist_subgenre = estimate_artist_genre(artist_name, genre_mapping)

        # Create genre directory
        genre_dir = os.path.join(out_dir, artist_genre, artist_subgenre)
        try:
            os.makedirs(genre_dir)
        except:
            print("Genre directory already exists.")

    # Create artist directory
    artist_dir = os.path.join(genre_dir, artist_name)
    try:
        os.mkdir(artist_dir)
    except:
        print("Artist directory already exists.")

    song_new_path = os.path.join(artist_dir, song_name + ".mid")
    shutil.copyfile(song, song_new_path)

    return song_new_path


if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='download_midi.py')
    parser.add_argument('--ms', type=str, required=True, help="Path to million song data.")
    parser.add_argument('--lakh', type=str, required=True, help="Path to the lakh dataset.")
    parser.add_argument('--genres', type=str, required=False, help="Path to the genres mapping.")
    parser.add_argument('--out', type=str, default=".", help="Output dir.")
    opt = parser.parse_args()

    # Load h5 info database
    songs = {}
    songs_info = load_song_info_database(opt.ms)

    # Load genres mapping
    genre_mapping = None
    with open(opt.genres) as f:
        genre_mapping = json.load(f)

    # Read all MIDI songs
    for dir_name, sub_dirs, files in os.walk(opt.lakh):
        if len(files) == 0:
            continue

        ms_song_id = dir_name.split("/")[-1]
        if ms_song_id not in songs_info:
            print("========== SONG", ms_song_id, "NOT IN SONGS INFO DATABASE ============")
            continue

        # A song directory might contain more than one version, select one
        selected_version_path = get_version_with_highest_unr(dir_name, files)
        #selected_version_md5 = os.path.splitext(selected_version_path)[0].split("/")[-1]

        with open(selected_version_path, "rb") as midi_file:
            selected_version_md5 = hashlib.md5(midi_file.read()).hexdigest()

        # Check for duplicates
        if selected_version_md5 not in songs:
            songs[selected_version_md5] = selected_version_path

            # Get song and artist names
            h5 = ms.hdf5_getters.open_h5_file_read(songs_info[ms_song_id])

            song_name = clean_name(ms.hdf5_getters.get_title(h5))
            artist_name = clean_name(ms.hdf5_getters.get_artist_name(h5))

            h5.close()

            print("Adding song", song_name, "by", artist_name)
            add_song(selected_version_path, song_name, artist_name, opt.out, genre_mapping)
