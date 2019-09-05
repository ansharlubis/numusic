import copy

class Player:
    def __init__(self, id):
        self.id = id
        self.instruments = set()
        self.beat_play = 0
        self.intervals = []
        self.can_assign = True
        self.redistributed = False

    def check_instrument(self, num):
        if self.can_assign:
            return True
        elif num in self.instruments:
            return True
        else:
            return False

    def add_interval(self, interval):
        self.intervals.append(interval)
        self.instruments.add(interval[2])
        if (len(self.instruments) == 3):
            self.can_assign = False
        self.beat_play += (interval[1]-interval[0]+1)
    
    def remove_interval(self, i):
        for interval in self.intervals:
            if (i[0] == interval[0]) and (i[1] == interval[1]) and (i[2] == interval[2]):
                self.intervals.remove(interval)
                self.beat_play -= (i[1]-i[0]+1)
        count = 0

        for interval in self.intervals:
            if i[2] == interval[2]:
                count += 1
        if count == 0:
            self.instruments.remove(i[2])
            self.can_assign = True

    def check_interval(self, check):
        for interval in self.intervals:
            if check[0] <= interval[0] and check[1] >= interval[0]:
                return False
            elif check[0] >= interval[0] and check[0] <= interval[1]:
                return False   
        return True

    def check_intervals(self, checks):
        for check in checks:
            if not self.check_interval(check):
                return False
        return True

    def __str__(self):
        return 'Player '+str(self.id)+', beats: '+str(self.beat_play)+', instruments: '+str(self.instruments)+'\nintervals: '+str(self.intervals)

    def __repr__(self):
        return str(self)

def depth(instruments_list, rest):
    song_length = len(instruments_list)

    intervals = [interval for interval_list in get_intervals(instruments_list, rest).values() for interval in interval_list]
    intervals = sorted(intervals, key=lambda interval: interval[0])

    depth = 0

    for i in range(0, song_length):
        temp = 0
        for interval in intervals:
            if i >= interval[0] and i <= interval[1]:
                temp += 1
        depth = max(temp, depth)

    return depth

def find_interval_end(copy_list, interval, current_instrument, rest):
    song_length = len(copy_list)
    start = interval[0]
    for i in range(start+1, len(copy_list)):
        if current_instrument in copy_list[i]:
            start += 1
            copy_list[i].remove(current_instrument)
        else:
            break
    interval.append(min(start+rest, song_length-1))
    return

def get_intervals_simple(instruments_list, rest):
    intervals = []
    copy_list = copy.deepcopy(instruments_list)
    for i in range(0, len(instruments_list)):
        for j in range(0, len(instruments_list[i])):
            current_instrument = instruments_list[i][j]
            if current_instrument in copy_list[i]:
                copy_list[i].remove(current_instrument)
                interval = [i]
                find_interval_end(copy_list, interval, current_instrument, rest)
                interval.append(current_instrument)
                intervals.append(interval)
            else:
                pass
    return intervals

# intervals is dictionary from instrument number to the interval
# of play
def get_intervals(instruments_list, rest):
    intervals = {}
    copy_list = copy.deepcopy(instruments_list)
    for i in range(0, len(instruments_list)):
        for j in range(0, len(instruments_list[i])):
            current_instrument = instruments_list[i][j]
            if current_instrument in copy_list[i]:
                
                # here the current instrument hasn't been involved in
                # an interval
                if current_instrument not in intervals.keys():
                    # this is the first time the particular instrument number
                    # is encountered
                    intervals[current_instrument] = []
                else:
                    # already encountered before
                    pass
                copy_list[i].remove(current_instrument)
                interval = [i]
                find_interval_end(copy_list, interval, current_instrument, rest)
                intervals[current_instrument].append(interval)
                
            else:
                # this means the current instrument has already been
                # part of an interval
                pass

    return intervals


################################################

# Assumptions:
# 1. Single copy for each instrument
def assignment_original(instruments_list, rest):
    i = 1
    intervals = get_intervals(instruments_list, rest)
    players = []

    for instrument in intervals.keys():
        unassignable_players = []
        players = sorted(players, key=lambda player: player.beat_play)

        for player in players:
            if player.can_assign:
                if player.check_intervals(intervals[instrument]):
                    for interval in intervals[instrument]:
                        interval.append(instrument)
                        player.add_interval(interval)
                    break
                else:
                    unassignable_players.append(player)
            else:
                unassignable_players.append(player)
    
        if len(unassignable_players) == len(players):
            new_player = Player(i)
            for interval in intervals[instrument]:
                interval.append(instrument)
                new_player.add_interval(interval)
            players.append(new_player)
            i += 1
        
        players = sorted(players, key=lambda player: player.beat_play)
    
    return sorted(players, key=lambda player: player.id)


####################################################     

# Assumptions:
# 1. Infinite number of instruments
# 2. Infinite number of instruments per person
def assignment_no_constraint(instruments_list, rest):
    i = 1
    intervals = get_intervals_simple(instruments_list, rest)
    players = []

    for interval in intervals:
        unassignable_players = []

        for player in players:
            if player.check_interval(interval):
                player.add_interval(interval)
                #print('assigning '+interval[2]+' to '+str(player.id))
                break
            else:
                unassignable_players.append(player)

        if len(unassignable_players) == len(players):
            new_player = Player(i)
            new_player.add_interval(interval)
            #print('assigning '+interval[2]+' to '+str(new_player.id))
            players.append(new_player)
            i += 1
        
        players = sorted(players, key=lambda player: player.beat_play)

    return sorted(players, key=lambda player: player.id)


######################################

# Assumption:
# 1. Infinite number of instruments
def assignment_limited_hand(instruments_list, rest):
    i = 1
    intervals = get_intervals_simple(instruments_list, rest)
    players = []

    for interval in intervals:
        unassignable_players = []

        for player in players:
            if player.can_assign or (interval[2] in player.instruments):
                if player.check_interval(interval):
                    player.add_interval(interval)
                    break
                else:
                    unassignable_players.append(player)
            else:
                unassignable_players.append(player)

        if len(unassignable_players) == len(players):
            new_player = Player(i)
            new_player.add_interval(interval)
            players.append(new_player)
            i += 1
        
        players = sorted(players, key=lambda player: player.beat_play)

    return sorted(players, key=lambda player: player.id)       


#######################################

def sort_intervals(length, intervals):
    result = []
    for i in range(0, length):
        current_intervals = [interval for interval in intervals if interval[0] == i]
        current_intervals = sorted(current_intervals, key=lambda interval: interval[1], reverse=True)
        result += current_intervals
    return result

def get_possible_players(interval, players):
    possible_players = []

    for player in players:
        if player.can_assign or (interval[2] in player.instruments):
            if player.check_interval(interval):
                possible_players.append(player)
    
    return possible_players

def overlapping(intervals, interval, player):
    for check in intervals:
        if check[2] in player.instruments:
            if check[0] >= interval[0] and check[0] <= interval[1]:
                return True
        elif check[0] > interval[1]:
            return False
        else:
            pass
    return False
    
def assignment_sub(intervals, interval, possible_players):
    assigned = []
    if len(possible_players) == 0:
        return assigned
    elif len(possible_players) == 1:
        assigned.append(possible_players[0])
        return assigned
    else:
        current_player = possible_players.pop(0)
        if interval[2] in current_player.instruments:
            assigned.append(current_player)
            return assigned
        elif overlapping(intervals, interval, current_player):
            return assignment_sub(intervals, interval, possible_players)
        else:
            assigned.append(current_player)
            return assigned

def assignment_improve(instruments_list, rest):
    i = 1
    song_length = len(instruments_list)
    intervals = sort_intervals(song_length, get_intervals_simple(instruments_list, rest))
    players = []

    for interval in intervals:
        # Give list of players that can be assigned with this interval
        possible_players = get_possible_players(interval, players)
        #print(interval)
        #print(possible_players)
        assigned = assignment_sub(intervals, interval, possible_players)

        if assigned:
            player = assigned[0]
            player.add_interval(interval)
            #print('assign to '+str(player.id))
        else:
            new_player = Player(i)
            new_player.add_interval(interval)
            #print('assign to '+str(new_player.id))
            players.append(new_player)
            i += 1

        players = sorted(players, key=lambda player: player.beat_play)
    
    return sorted(players, key=lambda player: player.id) 

#########################################