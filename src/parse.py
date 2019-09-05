from header import *
from block import *
from assignment import *
from optimization import optimize
from time import time
import sys

def parse(path):
	data = open(path, 'r')
	key = meta_data(parse_header(data))[1]
	instruments_list = parse_score(data).flatten().to_instrument(key).single_list()
	return instruments_list

def main():
	instruments_list = parse(sys.argv[1])
	initial_assignment = assignment_original(instruments_list, 1)
	optimized = optimize(initial_assignment, instruments_list, 1)

	for player in optimized:
		print(player)
		print()

if __name__ == "__main__":
    main()