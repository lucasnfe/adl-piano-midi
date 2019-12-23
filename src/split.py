import os
import random
import argparse
import shutil

from utils import get_midi_files

# Parse arguments
parser = argparse.ArgumentParser(description='download_midi.py')
parser.add_argument('--adl', type=str, required=True, help="Path of the adl data.")
parser.add_argument('--perc', type=float, default=0.1, help="Percentage of files for test set.")
parser.add_argument('--out', type=str, default=".", help="Output dir.")
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

n_midis = 0
midi_dirs = {}

for dir_name, sub_dirs, files in os.walk(opt.adl):
    if len(files) == 0:
        continue

    # Parse genre from directory name
    genre = dir_name[len(opt.adl):].split("/")[-3]

    if genre not in midi_dirs:
        midi_dirs[genre] = []

    for file_name in get_midi_files(files):
        midi_dirs[genre].append(os.path.join(dir_name, file_name))
        n_midis += 1

# Create train and test splits
try:
    os.mkdir(train_dir)
except OSError:
    print("Could not create train directory")

try:
    os.mkdir(test_dir)
except OSError:
    print("Could not create test directory")

random.seed(42)

c_dir = 0
dirs_list = list(midi_dirs.keys())

print(dirs_list)

while len(os.listdir(test_dir)) < int(opt.perc * n_midis):
    genre = dirs_list[c_dir]

    # Copy a random file from the adl dataset and add it to the list of test midis
    if len(midi_dirs[genre]) > 0:
        r = random.randint(0, len(midi_dirs[genre]) - 1)
        r_file = midi_dirs[genre].pop(r)

        shutil.copyfile(r_file, os.path.join(test_dir, os.path.basename(r_file)))

    c_dir = (c_dir + 1) % len(dirs_list)

for files in midi_dirs.values():
    for midi in files:
        shutil.copyfile(midi, os.path.join(train_dir, os.path.basename(midi)))

print("Total files:", n_midis)
print("Train", len(os.listdir(train_dir)))
print("Test", len(os.listdir(test_dir)))
