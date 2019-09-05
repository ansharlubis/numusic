import re
from measure import Measure
from voice import Voice
 
class Score:
    def __init__(self):
        self.list_of_measure = []

    def add_measure(self, measure):
        self.list_of_measure.append(measure)
    
    # Side-effect: changes * into the its previous tone
    def convert_asterisk(self):
        for measure in self.list_of_measure:
            measure.convert_asterisk()

    # Return a new score without jump attribute attached
    def remove_jump(self):
        score = Score()
        pattern_1 = re.compile(r'^%(\w+)')
        pattern_2 = re.compile(r'^to%(\w+)')
        jump_target = ''
        search_end = False
        for measure in self.list_of_measure:
            copy_measure = measure
            if search_end == False:
                filtered_att_1 = list(filter(pattern_1.match, measure.list_of_attribute))            
                if filtered_att_1 != []:
                    jump_target = pattern_1.search(filtered_att_1[0]).group(1)
                    search_end = True
                    copy_measures = []
                    copy_measure = measure.remove_attribute(filtered_att_1)
                    copy_measures.append(copy_measure)
                    score.add_measure(copy_measure)
                else:
                    score.add_measure(copy_measure)
            else:
                filtered_att_2 = list(filter(pattern_2.match, measure.list_of_attribute))
                if filtered_att_2 != []:
                    jump_var = re.search(pattern_2, filtered_att_2[0]).group(1)
                    if jump_var == jump_target:
                        search_end = False
                        copy_measure = measure.remove_attribute(filtered_att_2)
                        for copy in copy_measures:
                            score.add_measure(copy)
                    else:
                        copy_measures.append(copy_measure)
                    score.add_measure(copy_measure)
                else:
                    copy_measures.append(copy_measure)
                    score.add_measure(copy_measure)
        return score     

    # Flatten the entire score => flatten all measures
    def flatten(self):
        score = Score()
        for measure in self.list_of_measure:
            flattened = measure.flatten()
            score.add_measure(flattened)
        return score

    # Convert the content of the whole score into instrument numbers
    # done after flattening the whole score.
    def to_instrument(self, key):
        score = Score()
        keys = ['G', 'G#', 'A', 'A#', 'B', 'C','C#', 'D', 'D#', 'E', 'F', 'F#']
        pattern = re.compile(r'key(\w+)')
        for measure in self.list_of_measure:
            filtered_att = list(filter(pattern.match, measure.list_of_attribute))
            if filtered_att != []:
                key = pattern.search(filtered_att[0]).group(1)
                if key not in keys:
                    raise ValueError('Key must be one of the 12 tonal keys.')
                else:
                    copy_measure = measure.remove_attribute(filtered_att)
                    score.add_measure(copy_measure.to_instrument(key))
            else:
                score.add_measure(measure.to_instrument(key))
        return score
        
    def single_list(self):
        result = []
        for measure in self.list_of_measure:
            for beat in measure.list_of_voice[0].list_of_beat:
                result.append(beat.list_of_instrument)
        return result

    def __str__(self):
        return str(self.list_of_measure)