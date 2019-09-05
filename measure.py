from voice import *

class Measure:
    def __init__(self):
        self.list_of_attribute = []
        self.list_of_voice = []

    def add_attribute(self, att):
        self.list_of_attribute.append(att)

    def set_attributes(self, atts):
        self.list_of_attribute = atts

    def add_voice(self, voice):
        self.list_of_voice.append(voice)

    def set_voices(self, voices):
        self.list_of_voice = voices

    # Side-effect: changes * into the its previous tone
    def convert_asterisk(self):
        for voice in self.list_of_voice:
            voice.convert_asterisk()

    # Erase the content of attribute_list from self.list_of_attribute
    def remove_attribute(self, attribute_list):
        measure = Measure()
        measure.list_of_voice = self.list_of_voice
        temp = self.list_of_attribute
        measure.list_of_attribute = [attribute for attribute in temp if attribute not in attribute_list]
        return measure

    # Flatten the voices inside a measure into one voice
    def flatten(self):
        joined_voices = []
        voice_num = len(self.list_of_voice)
        if voice_num == 1:
            joined_voices.append(self.list_of_voice[0])
        else:
            temp_voice = self.list_of_voice[0]
            for i in range(1, voice_num):
                temp_voice = temp_voice.merge(self.list_of_voice[i])
            joined_voices.append(temp_voice)
        measure = Measure()
        measure.set_voices(joined_voices)
        measure.set_attributes(self.list_of_attribute)
        return measure

    # Convert the content of the measure into instrument numbers
    def to_instrument(self, key):
        measure = Measure()
        measure.set_attributes(self.list_of_attribute)
        for voice in self.list_of_voice:
            measure.add_voice(voice.to_instrument(key))
        return measure
        
    def __str__(self):
        result = ''
        result += str(self.list_of_attribute)
        result += '\n'
        for voice in self.list_of_voice:
            result += str(voice)
            result += '\n'
        return result
    
    def __repr__(self):
        return str(self)
  