import os
import random
import argparse
import shutil

from load import *

def adl_split(adl_dataset, p):
    random.seed(42)

    # Get songs by genre
    songs_by_genre = adl_songs_by_genre(adl_dataset)

    # Compute amount of test songs
    total_songs = sum([len(songs) for songs in songs_by_genre.values()])
    n_test_songs = int(total_songs * p)

    # Get list of genres
    genres_list = list(songs_by_genre.keys())

    train, test = [], []

    # Add songs by genre to the test split
    for i in range(n_test_songs):
        genre = genres_list[i % len(genres_list)]

        # Copy a random file from the adl dataset and add it to the list of test midis
        if len(songs_by_genre[genre]) > 0:
            r = random.randint(0, len(songs_by_genre[genre]) - 1)
            r_file = songs_by_genre[genre].pop(r)
            test.append(r_file)

    # Add the remaining songs to the train split
    for songs in songs_by_genre.values():
        train += songs

    return train, test

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='download_midi.py')
    parser.add_argument('--adl', type=str, required=True, help="Path of the adl data.")
    parser.add_argument('--out', type=str, default=".", help="Output dir.")
    parser.add_argument('--p', type=float, default=0.1, help="Percentage of files for test set.")
    opt = parser.parse_args()

    train_dir = os.path.join(opt.out, "train")
    test_dir = os.path.join(opt.out, "test")

    # Remove previous splits
    try:
        shutil.rmtree(train_dir)
    except OSError:
        pass

    try:
        shutil.rmtree(test_dir)
    except OSError:
        pass

    adl_dataset = adl_load_dataset(opt.adl)
    adl_dataset_stats = adl_stats(adl_dataset)

    train, test = adl_split(adl_dataset, opt.p)

    # Sum of splits should have same amount of songs in the dataset
    assert len(train) + len(test) == adl_dataset_stats["Songs"]

    # Create train and test splits
    try:
        os.makedirs(train_dir)
    except OSError:
        print("Could not create train directory")

    for song in train:
        song_name = song.split("/")[-1]
        shutil.copyfile(song, os.path.join(train_dir, song_name))

    try:
        os.makedirs(test_dir)
    except OSError:
        print("Could not create test directory")

    for song in test:
        song_name = song.split("/")[-1]
        shutil.copyfile(song, os.path.join(test_dir, song_name))

    print("Total files:", adl_dataset_stats["Songs"])
    print("Train", len(train))
    print("Test", len(test))
