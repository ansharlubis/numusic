import copy
from assignment import *

# return a list of intervals that player owns which
# overlap with interval
def overlapping_intervals(interval, player):
	overlapping = []
	for check in player.intervals:
		if (interval[2] != check[2]):
			if (interval[0] <= check[1]) and (interval[1] >= check[0]):
				overlapping.append(check)
	return overlapping

# remove to_remove from a list_of_players
# using deep copy -> no side-effect
def remove_player(to_remove, list_of_players):
	result = copy.deepcopy(list_of_players)
	for player in result:
		if player.id == to_remove.id:
			result.remove(player)
	return result

# renaming player so it becomes incremental again
# after optimization
def rename_player(opt):
	for i in range(1, len(opt)+1):
		opt[i-1].id = i
	return opt

def redistribute_instruments(player, original_list):
	redistribution_list = copy.deepcopy(original_list)
	redistribution_list = remove_player(player, redistribution_list)

	mutable_player = copy.deepcopy(player)

	count = 0
	interval_num = len(player.intervals)

	for target_player in redistribution_list:
		for interval in mutable_player.intervals:
			overlapping = overlapping_intervals(interval, target_player)
			if not overlapping:
				if target_player.check_instrument(interval[2]):
					target_player.add_interval(interval)
					mutable_player.remove_interval(interval)
					count += 1
				else:
					pass
			else:
				sub_redistribution_list = copy.deepcopy(redistribution_list)
				sub_redistribution_list = remove_player(target_player, sub_redistribution_list)

				mutable_target_player = copy.deepcopy(target_player)

				sub_count = 0
				sub_interval_num = len(overlapping)

				for sub_target_player in sub_redistribution_list:
					for sub_interval in overlapping:
						sub_overlapping = overlapping_intervals(sub_interval, sub_target_player)
						if not sub_overlapping:
							if sub_target_player.check_instrument(sub_interval[2]):
								sub_target_player.add_interval(sub_interval)
								mutable_target_player.remove_interval(sub_interval)
								overlapping.remove(sub_interval)
								sub_count += 1
							else:
								pass
						else:
							pass
					
					if sub_count == sub_interval_num:
						break
				
				if sub_count == sub_interval_num:
					if mutable_target_player.check_instrument(interval[2]):
						target_player = copy.deepcopy(mutable_target_player)
						target_player.add_interval(interval)
						mutable_player.remove_interval(interval)
						redistribution_list = copy.deepcopy(sub_redistribution_list)
						redistribution_list.append(target_player)
						redistribution_list = sorted(redistribution_list, key=lambda player: player.beat_play)
						count += 1

		if count == interval_num:
			break

	if count != interval_num:
		return sorted(original_list, key=lambda player: player.beat_play)
	elif mutable_player.intervals == []:
		return sorted(redistribution_list, key=lambda player: player.beat_play)

def optimize(initial_assignment, instruments_list, rest):

	score_depth = depth(instruments_list, rest)
	assignment = sorted(initial_assignment, key=lambda player: player.beat_play)

	i = 0

	while (i < len(assignment)):
		if len(assignment) == score_depth:
			break
		
		j = 0

		while (j < len(assignment)):
			if assignment[j].redistributed == False:
				assignment = redistribute_instruments(assignment[j], assignment)
				assignment[j].redistributed = True
				j = 0
				i += 1
				break
			else:
				j += 1

	return rename_player(sorted(assignment, key=lambda player: player.id))