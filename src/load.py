import os
import json
import argparse
import hashlib

from utils import get_midi_files

def adl_load_dataset(adl_path):
    adl_dataset = {}

    # Read all MIDI songs
    for dir, _ , files in os.walk(adl_path):
        if len(files) == 0:
            continue

        artist_name     = dir.split("/")[-1]
        artist_subgenre = dir.split("/")[-2]
        artist_genre    = dir.split("/")[-3]

        # Add full path to all midi files
        full_path_files = []
        for filename in get_midi_files(files):
            full_path_files.append(os.path.join(dir, filename))

        if artist_genre not in adl_dataset:
            adl_dataset[artist_genre] = {artist_subgenre: {artist_name: full_path_files}}
        else:
            if artist_subgenre not in adl_dataset[artist_genre]:
                adl_dataset[artist_genre][artist_subgenre] = {artist_name: full_path_files}
            else:
                if artist_name not in adl_dataset[artist_genre][artist_subgenre]:
                    adl_dataset[artist_genre][artist_subgenre][artist_name] = full_path_files
                else:
                    adl_dataset[artist_genre][artist_subgenre][artist_name] += full_path_files

    return adl_dataset

def adl_songs(adl_dataset):
    songs = {}
    for genre in adl_dataset:
        for subgenre in adl_dataset[genre]:
            for artist in adl_dataset[genre][subgenre]:
                for song_path in adl_dataset[genre][subgenre][artist]:
                    with open(song_path, "rb") as midi_file:
                        midi_md5 = hashlib.md5(midi_file.read()).hexdigest()

                        if midi_md5 not in songs:
                            songs[midi_md5] = song_path
                        else:
                            raise Exception('There is duplicated files in the dataset.')
    return songs

def adl_songs_by_genre(adl_dataset):
    songs_by_genre = {}

    for song_md5, song_path in adl_songs(adl_dataset).items():
        genre = song_path.split("/")[-3]

        if genre not in songs_by_genre:
            songs_by_genre[genre] = []

        songs_by_genre[genre].append(song_path)

    return songs_by_genre

def adl_stats(adl_dataset):
    current_midi_data_stats = {"Artists": 0, "Genres": 0, "Sub-Genres": 0, "Songs": 0}

    for genre in adl_dataset:
        current_midi_data_stats["Genres"] += 1
        for subgenre in adl_dataset[genre]:
            current_midi_data_stats["Sub-Genres"] += 1
            for artist in adl_dataset[genre][subgenre]:
                current_midi_data_stats["Artists"] += 1
                for songs in adl_dataset[genre][subgenre][artist]:
                    current_midi_data_stats["Songs"] += 1

    return current_midi_data_stats

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='download_midi.py')
    parser.add_argument('--adl', type=str, required=True, help="Path to the adl dataset.")
    opt = parser.parse_args()

    adl_dataset = adl_load_dataset(opt.adl)

    adl_dataset_stats = adl_stats(adl_dataset)
    print(adl_dataset_stats)

    adl_dataset_songs_by_genre = adl_songs_by_genre(adl_dataset)
    for genre, songs in adl_dataset_songs_by_genre.items():
        print(genre, ":", len(songs))
