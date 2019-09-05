from beat import *

class Voice:
    def __init__(self):
        self.list_of_beat = []
    
    def add_beat(self, beat):
        self.list_of_beat.append(beat)

    def set_beats(self, beats):
        self.list_of_beat = beats

   # Side-effect: changes * into the its previous tone
    def convert_asterisk(self):
        cur_tone = Tone(Normal(), 0, 0)
        for beat in self.list_of_beat:
            for tone in beat.list_of_tone:
                if tone.note == -1:
                    tone.change_tone(cur_tone)
                else:
                    cur_tone = tone    

    # Merge two voices
    def merge(self, other_voice):
        this_beats = self.list_of_beat
        that_beats = other_voice.list_of_beat
        joined_beats = [this.merge(that) for (this, that) in zip(this_beats, that_beats)]
        voice = Voice()
        voice.set_beats(joined_beats)
        return voice

    # Change the tones in the beats into instrument numbers
    def to_instrument(self, key):
        voice = Voice()
        for beat in self.list_of_beat:
            voice.add_beat(beat.to_instrument(key))
        return voice

    def __str__(self):
        return str(self.list_of_beat)

    def __repr__(self):
        return str(self)
