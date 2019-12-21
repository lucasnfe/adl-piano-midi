import os
import random
import argparse
import shutil

MIDI_EXTENSIONS = [".mid", ".midi", ".MID", ".MIDI"]

# Parse arguments
parser = argparse.ArgumentParser(description='download_midi.py')
parser.add_argument('--data', type=str, required=True, help="Path of the data.")
parser.add_argument('--perc', type=float, default=0.1, help="Percentage of files for test set.")
opt = parser.parse_args()

try:
    shutil.rmtree("train")
except OSError:
    pass

try:
    shutil.rmtree("test")
except OSError:
    pass

n_midis = 0
midi_dirs = {}

for dir in list(os.walk(opt.data)):
    dir_name, sub_dirs, files = dir

    midi_dirs[dir_name] = []

    for file_name in files:
        file_path = os.path.join(dir_name, file_name)
        _, extension = os.path.splitext(file_path)

        if extension in MIDI_EXTENSIONS:
            midi_dirs[dir_name].append(file_path)
            n_midis += 1

# Create train and test
try:
    os.mkdir("train")
except OSError:
    print("Could not create train directory")

try:
    os.mkdir("test")
except OSError:
    print("Could not create test directory")

random.seed(42)

c_dir = 0
dirs_list = list(midi_dirs.keys())

print(dirs_list)

while len(os.listdir("test")) < int(opt.perc * n_midis):
    dir_name = dirs_list[c_dir]

    # Remove a random file from the dir and add it to the list of test midis
    if len(midi_dirs[dir_name]) > 0:
        r = random.randint(0, len(midi_dirs[dir_name]) - 1)
        r_file = midi_dirs[dir_name].pop(r)
        
        shutil.copyfile(r_file, os.path.join("test", os.path.basename(r_file)))

    c_dir = (c_dir + 1) % len(dirs_list)

for files in midi_dirs.values():
    for midi in files:
        shutil.copyfile(midi, os.path.join("train", os.path.basename(midi)))

print("Total files:", n_midis)
print("Train", len(os.listdir("train")))
print("Test", len(os.listdir("test")))
