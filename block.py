from score import Score
from measure import Measure
from voice import Voice
from beat import Beat
from tone import *
import re

# Convert digit to tone
def digit_to_tone(digit_group):
    if digit_group[0] == '':
        pitch = Normal()
    elif digit_group[0] == '/':
        pitch = Sharp()
    else:
        pitch = Flat()

    if digit_group[1] == '*':
        tone = -1
    else:
        tone = int(digit_group[1])

    if ',' in digit_group[2]:
        octave = len(digit_group[2])*(-1)
    elif '\'' in digit_group[2]:
        octave = len(digit_group[2])
    else:
        octave = 0

    return Tone(pitch, tone, octave)

def beats_to_voice(beats):
    result = Voice()
    for beat in beats:
        cur_beat = Beat()
        tones = re.findall(r'(\\|/)?([0-7\*])(\,|\')*', beat)
        for group_digit in tones:
            cur_beat.add_tone(digit_to_tone(group_digit))
        result.add_beat(cur_beat)
    return result

# Convert a parsed block into a list of measures
# Side-effect: measures are appended into score
def make_score(score, parsed_block, bar_to_att):
    measure_len = len(parsed_block[0])
    for measure_num in range(0, measure_len):
        cur_measure = Measure()
        measure_width = len(parsed_block)
        for voice_num in range(0, measure_width):
            cur_measure.add_voice(beats_to_voice(parsed_block[voice_num][measure_num]))
        if measure_num in bar_to_att:
            for attribute in bar_to_att[measure_num]:
                cur_measure.add_attribute(attribute)
        score.add_measure(cur_measure)
    return score

# Get a map from bar to its attributes
def attribute_bar(block):
    next_line = block[1]

    bar_search = re.finditer(r'\|', next_line)
    bar_pos = [m.start() for m in bar_search]

    attributes = re.finditer(r'(%\w+)|(key\w+)|(to%\w+)', block[0])
    bar_to_att = {}
    for num in range(0, len(bar_pos)-1):
        bar_to_att[num] = []

    for att in attributes:
        att_pos = att.start()
        att_dis = [abs(att_pos-bar) for bar in bar_pos]
        closest = att_dis.index(min(att_dis))
        bar_to_att[closest].append(att.group())

    return bar_to_att

# Convert a block into List[List[Beat]]
def parse_block(block):
    dup = block
    dup.pop(0)
    y = [dup[i] for i in range(0, len(dup)) if i%2==1]
    z = [v.split('|') for v in y]
    
    result = []

    for line in z:
        temp = [grp.strip().split() for grp in line if not re.match(r'^\s*$|\s*\n', grp) ]
        result.append(temp)

    return result

# Grab blocks of notes from the score
def text_to_blocks(data):
    result = []
    block_flag = False

    for line in data.readlines():
        if re.match(r'\s*\n', line) and block_flag == False:
            pass
        elif re.search(r'key|%', line) and block_flag == False:
            block_flag = True
            block = []
            block.append(line)
        elif re.search(r'\|', line) and block_flag == False:
            block_flag = True
            block = []
            block.append('\n')
            block.append(line)
        elif re.search(r'\|', line) and block_flag == True:
            block.append(line)
        elif re.match(r'\s*\n', line) and block_flag == True:
            block_flag = False
            result.append(block)
        elif re.search(r'key|%', line) and block_flag == True:
            result.append(block)
            block = []
            block.append(line)
    result.append(block)

    return result

def parse_score(data):
	blocks = text_to_blocks(data)
	score = Score()
	for block in blocks:
		attributes = attribute_bar(block)
		parsed_block = parse_block(block)
		score = make_score(score, parsed_block, attributes)
	score.convert_asterisk()
	return score