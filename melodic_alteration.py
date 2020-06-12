import random

from modes_and_keys import apply_key, Modes, Starting_Pitch
from rhythm import merge_pitches_with_rhythm

test_pieces = {
    'A': 'note qn 71 :+: note qn 70 :+: note hn 66 :+: note qn 71 :+: note en 75 :+: note en 76 :+: note en 75 :+: note en 73 :+: note en 68 :+: note en 71 :+: note en 73 :+: note en 71 :+: note en 70 :+: note en 73 :+: note en 70 :+: note en 76 :+: note en 73 :+: note en 70 :+: note en 66 :+: note en 68 :+: note en 66 :+: note en 64 :+: note en 64 :+: note en 64', 
    'B': 'note en 71 :+: note en 71 :+: note en 75 :+: note en 71 :+: note en 73 :+: note en 75 :+: note en 76 :+: note en 76 :+: note en 80 :+: note en 83 :+: note en 80 :+: note en 73 :+: note en 76 :+: note en 80 :+: note en 78 :+: note en 82 :+: note en 78 :+: note en 76 :+: note en 73 :+: note en 76 :+: note en 80 :+: note en 76 :+: note en 73 :+: note en 76'
}

testy = "note qn 64 :+: note qn 72 :+: note qn 72 :+: note hn 72 :+: note qn 72 :+: note qn 71 :+: note qn 65 :+: note qn 71 :+: note hn 72 :+: note qn 67 :+: note qn 67 :+: note qn 69 :+: note qn 67 :+: note hn 60 :+: note qn 60 :+: note qn 60 :+: note qn 67 :+: note qn 67 :+: note hn 60 :+: note qn 58 :+: note qn 69 :+: note qn 73 :+: note qn 69 :+: note hn 69 :+: note qn 71 :+: note qn 69 :+: note qn 60 :+: note qn 52 :+: note hn 52 :+: note qn 55 :+: note qn 62 :+: note qn 72 :+: note qn 65 :+: note hn 57 :+: note qn 64 :+: note qn 64 :+: note qn 60 :+: note qn 57 :+: note hn 62 :+: note qn 62 :+: note qn 62 :+: note qn 67 :+: note qn 71 :+: note qn 64 :+: note qn 72 :+: note qn 72 :+: note hn 72 :+: note qn 72 :+: note qn 71 :+: note qn 65 :+: note qn 71 :+: note hn 72 :+: note qn 67 :+: note qn 67 :+: note qn 69 :+: note qn 67 :+: note hn 60 :+: note qn 60 :+: note qn 60 :+: note qn 67 :+: note qn 67 :+: note hn 60 :+: note qn 58 :+: note qn 69 :+: note qn 73 :+: note qn 69 :+: note hn 69 :+: note qn 71 :+: note qn 69 :+: note qn 60 :+: note qn 52 :+: note hn 52 :+: note qn 55 :+: note qn 62 :+: note qn 72 :+: note qn 65 :+: note hn 57 :+: note qn 64 :+: note qn 64 :+: note qn 60 :+: note qn 57 :+: note hn 62 :+: note qn 62 :+: note qn 62 :+: note qn 67 :+: note qn 71:+: note wn 64"

def strip_part(part):
    rhythm = []
    pitches = []
    for bit in part.split(' '):
        if bit.isdigit():
            pitches.append(int(bit))
        elif bit != ":+:" and bit != "note":
            rhythm.append(bit)
    return (pitches, rhythm)


def infer_key(pitches):
    possibilities = [[apply_key(mode, pitch) for mode in Modes]
                                             for pitch in Starting_Pitch]
    possibilities = sum(possibilities, [])
    probabilities = {}
    for key in possibilities:
        mode = key[1][0]
        base = key[1][1]
        fuller_mode = [j + base for j in sum(list(map(lambda x: 
                                                  [i + 12*x for i in mode],
                                                           range(-3,2))),[])]
        score = 0
        for pitch in pitches:
            if pitch in fuller_mode:
                score += 1
        probabilities[key[0]] = score
    return max(probabilities, key=probabilities.get)

# print(strip_part(test_pieces['A'])[0])
# print(infer_key(strip_part(testy)[0]))

def find_bridge(start, goal, length, fuller_mode):
    if goal not in fuller_mode:
        fuller_mode.append(goal)
        fuller_mode.sort()
        goal_index = fuller_mode.index(goal)
        fuller_mode.remove(goal)
    else:
        goal_index = fuller_mode.index(goal)
    if start not in fuller_mode:
        fuller_mode.append(start)
        fuller_mode.sort()
        start_index = fuller_mode.index(start)
        fuller_mode.remove(start)
    else:
        start_index = fuller_mode.index(start)
    if goal_index > start_index:
        path = fuller_mode[start_index:goal_index]
    else:
        path = fuller_mode[goal_index:start_index+1]
        path.reverse()
    if length == 1:
        return path[int(len(path)/2)]
    elif length == len(path):
        return path
    elif length == len(path)-1:
        return path[1:]
    elif length == len(path)-2:
        return path[1:-1]
    elif length == len(path)*2:
        return [val for val in path for _ in (0,1)]
    elif length < len(path):
        path = path[1:-1]
        while len(path) != length:
            path.remove(random.choice(path))
        return path
    else:
        # duplicate an element at random
        while len(path) != length:
            if len(path) > 2:
                element = random.choice(path[1:-1])
            elif len(path) > 1:
                element = random.choice(path[1:])
            else:
                element = random.choice(path)
            path.insert(path.index(element), element)
        return path



def check_space_for_insert(start, goal, fuller_mode, min_distance):
    if goal not in fuller_mode:
        fuller_mode.append(goal)
        fuller_mode.sort()
        goal_index = fuller_mode.index(goal)
        fuller_mode.remove(goal)
    else:
        goal_index = fuller_mode.index(goal)
    if start not in fuller_mode:
        fuller_mode.append(start)
        fuller_mode.sort()
        start_index = fuller_mode.index(start)
        fuller_mode.remove(start)
    else:
        start_index = fuller_mode.index(start)
    return abs(goal_index - start_index) > min_distance


def insert_passing_tones(sequence, min_distance):
# How to infer applied_key from only chord progression??
    applied_key = apply_key("Ionian", "C")
    mode = applied_key[1][0]
    base = applied_key[1][1]
    fuller_mode = [j + base for j in sum(list(map(lambda x: 
                                                  [i + 12*x for i in mode],
                                                           range(-3,2))),[])]
    to_insert = []
    for i in range(0, len(sequence[0])-1):
        if check_space_for_insert(sequence[0][i], sequence[0][i+1],
                                          fuller_mode, min_distance):
            pitch = find_bridge(sequence[0][i], sequence[0][i+1], 1, fuller_mode)
            to_insert.append([pitch, i+1])

    for i in range(len(to_insert)):
        sequence[0].insert(to_insert[i][1]+i, to_insert[i][0])
    # print(sequence[0])

# insert_passing_tones(strip_part(test_pieces['A']), 2)

def is_rhythm_constant(sequence):
    return sequence[1][1:] == sequence[1][:-1]

def is_trillable(sequence):
    for i in range(len(sequence[0])-1):
        if sequence[0][i] - sequence[0][i+1] < 6:
            return True
    return False


def alterate_part(part):
    sequence = strip_part(part)
    alteration = random.choice(['retrograde', 'trills'])#, 'invert'])
    if is_trillable(sequence) and alteration == 'trills':
        r = random.choice([1, 2, 3])
        if r == 1:
            sequence = add_quarter_trills(sequence)
        elif r == 2:
            sequence = add_eighth_trills(sequence)
        else:
            sequence = add_quarter_trills(sequence)
            sequence = add_eighth_trills(sequence)
    else: #if alteration == 'retrograde':
        r = random.choice([1, 2, 3])
        if r == 1 and not is_rhythm_constant(sequence):
            sequence = retrograde_only_rhythm(sequence)
        elif r == 2:
            sequence = retrograde_with_rhythm(sequence)
        else:
            sequence = retrograde_without_rhythm(sequence)
    # else:
        # sequence = invert(sequence)
    return merge_pitches_with_rhythm(sequence[0], sequence[1])

# ---------Alterations--------- #

# Returns the reverse of the sequence
def retrograde_with_rhythm(sequence):
    return (sequence[0][::-1], sequence[1][::-1])

def retrograde_without_rhythm(sequence):
    return (sequence[0][::-1], sequence[1])

def retrograde_only_rhythm(sequence):
    return (sequence[0], sequence[1][::-1])

# TODO: Make this sound good
# Returns the inverse (centered around the tonic, assumed to be the first)
# of the sequence
def invert(sequence):
    result = []
    tonic = sequence[0][0]
    return ([tonic - sequence[0][i] + tonic for i in range(len(sequence[0]))],
                                                                   sequence[1])

def insert_n_trills(sequence, i, n, note):
    first_pitch  = sequence[0].pop(i)
    second_pitch = sequence[0].pop(i)
    sequence[1].pop(i)
    sequence[1].pop(i)
    [sequence[0].insert(i, second_pitch)  for j in range(0, n)]
    [sequence[0].insert(i+j, first_pitch) for j in range(0, n*2, 2)]
    [sequence[1].insert(i+j, 'en') for j in range(0, n*2)]
    return sequence


# Replaces longer notes with connecting trills
def add_quarter_trills(sequence):
    for i in range(len(sequence[0])-1):
        if sequence[0][i] - sequence[0][i+1] < 6:
            if sequence[1][i] == 'hn' == sequence[1][i+1]:
                sequence = insert_n_trills(sequence, i, 2, 'qn')
    return sequence


def add_eighth_trills(sequence):
    for i in range(len(sequence[0])-1):
        if sequence[0][i] - sequence[0][i+1] < 6:
            if ((sequence[1][i] == 'hn' and sequence[1][i+1] == 'qn') or \
                (sequence[1][i] == 'qn' and sequence[1][i+1] == 'hn')):
                sequence = insert_n_trills(sequence, i, 3, 'en')
            elif sequence[1][i] == 'qn' == sequence[1][i+1]:
                sequence = insert_n_trills(sequence, i, 2, 'en')
    return sequence