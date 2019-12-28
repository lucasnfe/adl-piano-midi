import os
import pretty_midi

VALID_NAME_CHARS = ["_", "-", "(", ")", ","]

MIDI_EXTENSIONS = [".mid", ".midi", ".MID", ".MIDI"]

def get_midi_files(files):
    midi_files = []
    for file_name in files:
        # Check if it is a midi file
        _, extension = os.path.splitext(file_name)
        if extension in MIDI_EXTENSIONS:
            midi_files.append(file_name)

    return midi_files

def has_two_hands(file_path):
    try:
        print("Parsing piano from file:", file_path)
        midi_data = pretty_midi.PrettyMIDI(file_path)
    except:
        print("Cannot open midi file:", file_path)
        return False

    for instrument in midi_data.instruments:
        note_starts = {}
        for n in instrument.notes:
            if n.start not in note_starts:
                note_starts[n.start] = n.pitch
            else:
                if abs(note_starts[n.start] - n.pitch) > 12:
                    return True

    return False

def clean_name(name):
    return ''.join(c for c in name if c.isalnum() or c.isspace() or c in VALID_NAME_CHARS)
