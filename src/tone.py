class Pitch:
    def __init__(self):
        pass

class Sharp(Pitch):
    def __str__(self):
        return '/'

class Flat(Pitch):
    def __str__(self):
        return '\\'

class Normal(Pitch):
    def __str__(self):
        return ''

class Tone:
    # pitch is either Sharp, Flat, or Normal
    # note is an integer more or equal 0 and less or equal 7
    # octave is represented by integer, 1 is high, -1 is low, 2 is double high, etc.
    def __init__(self, pitch, note, octave):
        if not isinstance(pitch, Pitch):
            raise ValueError('Not a pitch')
        if note < -1 or note > 7:
            raise ValueError('Not a correct notation')
        self.pitch = pitch
        self.note = note
        self.octave = octave

    def equal(self, other_tone):
        if (isinstance(self.pitch, type(other_tone.pitch)) and self.note == other_tone.note 
            and self.octave == other_tone.octave):
            return True
        elif (isinstance(self.pitch, type(Sharp())) and isinstance(other_tone.pitch, type(Flat())) and 
            self.note == other_tone.note-1 and self.octave == other_tone.octave):
            return True
        elif (isinstance(self.pitch, type(Flat())) and isinstance(other_tone.pitch, type(Sharp())) and 
            self.note == other_tone.note+1 and self.octave == other_tone.octave):
            return True
        else:
            return False

    def change_tone(self, other_tone):
        self.pitch = other_tone.pitch
        self.note = other_tone.note
        self.octave = other_tone.octave

    def next_tone(self):
        if self.note == 0:
            return self
        else:
            if isinstance(self.pitch, type(Normal())):
                if self.note in [1, 2, 4, 5, 6]:
                    return Tone(Sharp(), self.note, self.octave)
                elif self.note == 3:
                    return Tone(Normal(), 4, self.octave)
                elif self.note == 7:
                    return Tone(Normal(), 1, self.octave+1)
                else:
                    raise ValueError('Invalid note.')
            elif isinstance(self.pitch, type(Sharp())):
                if self.note in [1, 2, 4, 5, 6]:
                    return Tone(Normal(), self.note+1, self.octave)
                else:
                    raise ValueError('Invalid sharp note.')
            elif isinstance(self.pitch, type(Flat())):
                if self.note in [2, 3, 5, 6, 7]:
                    return Tone(Normal(), self.note, self.octave)
                else:
                    raise ValueError('Invalid flat note.')

    def previous_tone(self):
        if self.note == 0:
            return self
        else:
            if isinstance(self.pitch, type(Normal())):
                if self.note in [2, 3, 5, 6, 7]:
                    return Tone(Sharp(), self.note-1, self.octave)
                elif self.note == 4:
                    return Tone(Normal(), 3, self.octave)
                elif self.note == 1:
                    return Tone(Normal(), 7, self.octave-1)
                else:
                    raise ValueError('Invalid note.')
            elif isinstance(self.pitch, type(Sharp())):
                if self.note in [1, 2, 4, 5, 6]:
                    return Tone(Normal(), self.note, self.octave)
                else:
                    raise ValueError('Invalid sharp note.')
            elif isinstance(self.pitch, type(Flat())):
                if self.note in [2, 3, 5, 6, 7]:
                    return Tone(Normal(), self.note-1, self.octave)
                else:
                    raise ValueError('Invalid flat note.')
    
    def previous_n_tone(self, n):
        result = self
        if n == 0:
            return result
        elif n == 1:
            return result.previous_tone()
        else:
            return result.previous_tone().previous_n_tone(n-1)

    def __str__(self):
        if self.octave < 0:
            return '{'+str(self.pitch)+str(self.note)+(abs(self.octave)*',')+'}'
        elif self.octave > 0:
            return '{'+str(self.pitch)+str(self.note)+(self.octave*'\'')+'}'
        else:
            return '{'+str(self.pitch)+str(self.note)+'}'
    
    def __repr__(self):
        return str(self)
