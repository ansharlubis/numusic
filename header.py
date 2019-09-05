import re

# Take a musical score data and grab the header
# File -> List[String]
def parse_header(data):
    header = []
    for line in data:
        if line == '\n':
            break
        if re.search(r'key|%',line):
            break
        header.append(line)
    return header

def header_check(time, time_f, key, key_f):
    if not time_f:
        raise(Exception('Time signature is not declared.'))
    if not key_f:
        raise(Exception('Key is not declared.'))
    if time == '':
        raise(Exception('Time signature is not declared properly.'))
    if key == '':
        raise(Exception('Key is not declared properly.'))
    return 0

# Get the time signature and starting key (clef) from the music score header
# List[String] -> List[Pair[Int], String]
def meta_data(header):
    time_found = False; key_found = False
    time = []; key = ''
    for line in header:
        time_check = re.match(r'Time:', line)
        key_check = re.match(r'Key:', line)
        if time_check:
            time_found = True
            time_match = re.match(r'Time:\s*(\d)/(\d)', line)
            if time_match:
                time.append(int(time_match.group(1)))
                time.append(int(time_match.group(2)))
        if key_check:
            key_found = True
            key_match = re.match(r'Key:\s*Do\s*=\s*(\S+)', line)
            if key_match:
                key = key_match.group(1)     
    header_check(time, time_found, key, key_found)
    return [time, key]