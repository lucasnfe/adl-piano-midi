import os
import argparse
import pretty_midi

from utils import get_midi_files

MIDI_PIANO_PROGRAMS = 8

def parse_piano(midi_data):
    instruments_to_remove = []

    for instrument in midi_data.instruments:
        if instrument.program > MIDI_PIANO_PROGRAMS or instrument.is_drum:
            instruments_to_remove.append(instrument)

    for i in instruments_to_remove:
        midi_data.instruments.remove(i)

    return midi_data

def has_chord(midi):
    for instrument in midi_data.instruments:
        note_starts = {}
        for n in instrument.notes:
            if n.start not in note_starts:
                note_starts[n.start] = n.pitch
            else:
                if abs(note_starts[n.start] - n.pitch) > 12:
                    return True

    return False

# Parse arguments
parser = argparse.ArgumentParser(description='download_midi.py')
parser.add_argument('--lakh', type=str, required=True, help="Path of the lakh dataset.")
parser.add_argument('--out', type=str, default=".", help="Output dir.")
opt = parser.parse_args()

for dir_name, sub_dirs, files in os.walk(opt.lakh):
    midi_files = get_midi_files(files)

    for midi_name in midi_files:
        file_path = os.path.join(dir_name, midi_name)

        try:
            print("Parsing piano from file:", file_path)
            midi_data = pretty_midi.PrettyMIDI(file_path)
        except:
            print("Cannot open midi file:", file_path)
            continue

        midi_data = parse_piano(midi_data)

        if len(midi_data.instruments) > 0 and has_chord(midi_data):
            new_path = dir_name[len(opt.lakh):]

            try:
                os.makedirs(os.path.join(opt.out, new_path))
            except FileExistsError:
                print("Directory already exists.")

            midi_data.write(os.path.join(opt.out, new_path, midi_name))
