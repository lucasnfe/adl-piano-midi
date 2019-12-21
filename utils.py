import os

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

def clean_name(name):
    return ''.join(c for c in name if c.isalnum() or c.isspace() or c in VALID_NAME_CHARS)
