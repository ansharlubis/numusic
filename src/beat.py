from tone import *

class Beat:
    def __init__(self):
        self.list_of_tone = []
        self.list_of_instrument = []

    def add_tone(self, tone):
        self.list_of_tone.append(tone)

    def set_tones(self, tones):
        self.list_of_tone = tones

    def remove_instrument(self, i):
        self.list_of_instrument.remove(i)

    def set_instruments(self, instruments):
        self.list_of_instrument = instruments
    
    # Merge two beats into one beat
    def merge(self, other_beat):
        joined_tones = self.list_of_tone + other_beat.list_of_tone
        beat = Beat()
        beat.set_tones(joined_tones)
        return beat

    # Change the tones into instrument numbers
    def to_instrument(self, key):
        beat = Beat()
        instrument = beat.tone_to_number(key)
        instrument_list = []
        for tone in self.list_of_tone:
            if tone.note != 0:
                if instrument[str(tone)] not in instrument_list:
                    instrument_list.append(instrument[str(tone)])
        beat.set_instruments(instrument_list)
        return beat

    # Returning a mapping from tone to instrument number
    def tone_to_number(self, key):
        keys = ['G', 'G#', 'A', 'A#', 'B', 'C','C#', 'D', 'D#', 'E', 'F', 'F#']
        distance = keys.index(key)
        initial = Tone(Normal(), 1, -1).previous_n_tone(distance)
        angklung_number = keys+[str(i) for i in range(1,31)]
        tone_number = []
        for i in range(0, len(angklung_number)):
            tone_number.append(str(initial))
            initial = initial.next_tone()
        return dict(zip(tone_number, angklung_number))

    def __str__(self):
        if self.list_of_instrument != []:
            return str(self.list_of_instrument)
        else:
            return str(self.list_of_tone)
    
    def __repr__(self):
        if self.list_of_instrument != []:
            return str(self.list_of_instrument)
        else:
            return str(self.list_of_tone)
