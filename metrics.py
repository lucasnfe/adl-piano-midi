import pretty_midi

def unique_notes_ratio(song_path):
    try:
        song_midi = pretty_midi.PrettyMIDI(song_path)
    except:
        return 0

    unique_notes = set()
    total_notes = []

    for instrument in song_midi.instruments:
        instrument_notes = [n.pitch for n in instrument.notes]
        unique_notes = unique_notes | set(instrument_notes)
        total_notes += instrument_notes

    return len(unique_notes)/len(total_notes)
