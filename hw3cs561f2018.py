# Denis Lim
# USC ID: 9523957111
# CSCI561 HW3
# November 16, 2018


# I think materials covered are up to lectures 20-21.
import sys
import numpy as np
import pprint

s = 0 # grid size
n = 0 # number of cars
o = 0 # number of obstacles
obstacles = [] # array of obstacle locations
carOrigins = [] # array of car start locations
carDestinations = [] # array of car destinations
carMap = [[]]

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

maps = {}

policiesDict = {}
# policies0 = [[None, left, left],
# 			[up, up, up],
# 			[right, up, up]]

policies0 = {
			(0,0): None,
			(1,0): left,
			(2,0): left,
			(0,1): up,
			(1,1): up,
			(2,1): up,
			(0,2): right,
			(1,2): up,
			(2,2): up
			}

policies1 = [{
	(7, 3): (0, -1),
	(6, 9): (-1, 0),
	(0, 7): (0, -1),
	(1, 6): (0, -1),
	(3, 7): (1, 0),
	(2, 5): (0, -1),
	(8, 5): (0, -1),
	(5, 8): (0, -1),
	(4, 0): (1, 0),
	(9, 0): (-1, 0),
	(6, 7): (0, -1),
	(5, 5): (0, -1),
	(7, 6): (0, -1),
	(0, 4): (0, -1),
	(1, 1): (1, 0),
	(3, 2): (1, 0),
	(2, 6): (0, -1),
	(8, 2): (0, -1),
	(4, 5): (0, -1),
	(9, 3): (0, -1),
	(6, 0): (1, 0),
	(7, 5): (0, -1),
	(0, 1): (1, 0),
	(3, 1): (1, 0),
	(9, 9): (-1, 0),
	(7, 8): (0, -1),
	(2, 1): (1, 0),
	(8, 9): (-1, 0),
	(9, 4): (0, -1),
	(5, 1): (1, 0),
	(7, 2): (0, -1),
	(1, 5): (0, -1),
	(3, 6): (0, -1),
	(2, 2): (1, 0),
	(8, 6): (-1, 0),
	(4, 1): (1, 0),
	(9, 7): (0, -1),
	(6, 4): (1, 0),
	(5, 4): (0, -1),
	(7, 1): None,
	(0, 5): (0, -1),
	(1, 0): (1, 0),
	(0, 8): (0, -1),
	(3, 5): (0, -1),
	(2, 7): (1, 0),
	(8, 3): (-1, 0),
	(4, 6): (0, -1),
	(9, 2): (0, -1),
	(6, 1): (1, 0),
	(5, 7): (0, -1),
	(7, 4): (0, -1),
	(0, 2): (1, 0),
	(1, 3): (1, 0),
	(4, 8): (0, -1),
	(3, 0): (1, 0),
	(2, 8): (1, 0),
	(9, 8): (0, -1),
	(8, 0): (-1, 0),
	(6, 2): (0, -1),
	(5, 0): (1, 0),
	(1, 4): (0, -1),
	(3, 9): (0, -1),
	(2, 3): (1, 0),
	(1, 9): (1, 0),
	(8, 7): (0, -1),
	(4, 2): (0, -1),
	(9, 6): (-1, 0),
	(6, 5): (1, 0),
	(5, 3): (0, -1),
	(7, 0): (0, 1),
	(6, 8): (0, -1),
	(0, 6): (0, -1),
	(1, 7): (-1, 0),
	(0, 9): (0, -1),
	(3, 4): (0, -1),
	(2, 4): (0, -1),
	(8, 4): (-1, 0),
	(5, 9): (-1, 0),
	(4, 7): (0, -1),
	(9, 1): (-1, 0),
	(6, 6): (0, -1),
	(5, 6): (0, -1),
	(7, 7): (0, -1),
	(0, 3): (0, -1),
	(1, 2): (1, 0),
	(4, 9): (0, -1),
	(3, 3): (0, -1),
	(2, 9): (1, 0),
	(8, 1): (-1, 0),
	(4, 4): (0, -1),
	(6, 3): (0, -1),
	(0, 0): (1, 0),
	(7, 9): (-1, 0),
	(3, 8): (1, 0),
	(2, 0): (1, 0),
	(1, 8): (1, 0),
	(8, 8): (-1, 0),
	(4, 3): (0, -1),
	(9, 5): (0, -1),
	(5, 2): (0, -1)},
	{(7, 3): (0, -1),
	(6, 9): (-1, 0),
	(0, 7): (0, -1),
	(1, 6): (0, -1),
	(3, 7): (1, 0),
	(2, 5): (0, -1),
	(8, 5): (-1, 0),
	(5, 8): (0, -1),
	(4, 0): (0, 1),
	(9, 0): (-1, 0),
	(6, 7): (0, -1),
	(5, 5): (0, -1),
	(7, 6): (-1, 0),
	(0, 4): (0, -1),
	(1, 1): (1, 0),
	(3, 2): (0, -1),
	(2, 6): (0, -1),
	(8, 2): (0, -1),
	(4, 5): (0, -1),
	(9, 3): (0, -1),
	(6, 0): (-1, 0),
	(7, 5): (-1, 0),
	(0, 1): (1, 0),
	(3, 1): (1, 0),
	(9, 9): (-1, 0),
	(7, 8): (0, -1),
	(2, 1): (1, 0),
	(8, 9): (-1, 0),
	(9, 4): (-1, 0),
	(5, 1): (-1, 0),
	(7, 2): (0, -1),
	(1, 5): (0, -1),
	(3, 6): (0, -1),
	(2, 2): (1, 0),
	(8, 6): (-1, 0),
	(4, 1): None,
	(9, 7): (0, -1),
	(6, 4): (-1, 0),
	(5, 4): (-1, 0),
	(7, 1): (-1, 0),
	(0, 5): (0, -1),
	(1, 0): (1, 0),
	(0, 8): (0, -1),
	(3, 5): (0, -1),
	(2, 7): (1, 0),
	(8, 3): (-1, 0),
	(4, 6): (0, -1),
	(9, 2): (0, -1),
	(6, 1): (-1, 0),
	(5, 7): (0, -1),
	(7, 4): (-1, 0),
	(0, 2): (1, 0),
	(1, 3): (1, 0),
	(4, 8): (0, -1),
	(3, 0): (1, 0),
	(2, 8): (1, 0),
	(9, 8): (-1, 0),
	(8, 0): (-1, 0),
	(6, 2): (-1, 0),
	(5, 0): (-1, 0),
	(1, 4): (0, -1),
	(3, 9): (0, -1),
	(2, 3): (0, -1),
	(1, 9): (1, 0),
	(8, 7): (-1, 0),
	(4, 2): (0, -1),
	(9, 6): (-1, 0),
	(6, 5): (-1, 0),
	(5, 3): (0, -1),
	(7, 0): (-1, 0),
	(6, 8): (-1, 0),
	(0, 6): (0, -1),
	(1, 7): (-1, 0),
	(0, 9): (0, -1),
	(3, 4): (0, -1),
	(2, 4): (0, -1),
	(8, 4): (-1, 0),
	(5, 9): (-1, 0),
	(4, 7): (0, -1),
	(9, 1): (0, -1),
	(6, 6): (-1, 0),
	(5, 6): (0, -1),
	(7, 7): (0, -1),
	(0, 3): (0, -1),
	(1, 2): (1, 0),
	(4, 9): (0, -1),
	(3, 3): (0, -1),
	(2, 9): (1, 0),
	(8, 1): (-1, 0),
	(4, 4): (0, -1),
	(6, 3): (-1, 0),
	(0, 0): (1, 0),
	(7, 9): (-1, 0),
	(3, 8): (0, -1),
	(2, 0): (1, 0),
	(1, 8): (1, 0),
	(8, 8): (-1, 0),
	(4, 3): (0, -1),
	(9, 5): (-1, 0),
	(5, 2): (0, -1)},
	{(7, 3): (0, -1),
	(6, 9): (-1, 0),
	(0, 7): (0, -1),
	(1, 6): (0, -1),
	(3, 7): (1, 0),
	(2, 5): (0, -1),
	(8, 5): (0, -1),
	(5, 8): (0, -1),
	(4, 0): (1, 0),
	(9, 0): None,
	(6, 7): (0, -1),
	(5, 5): (0, -1),
	(7, 6): (0, -1),
	(0, 4): (0, -1),
	(1, 1): (1, 0),
	(3, 2): (0, -1),
	(2, 6): (0, -1),
	(8, 2): (0, -1),
	(4, 5): (0, -1),
	(9, 3): (0, -1),
	(6, 0): (1, 0),
	(7, 5): (0, -1),
	(0, 1): (1, 0),
	(3, 1): (1, 0),
	(9, 9): (-1, 0),
	(7, 8): (0, -1),
	(2, 1): (1, 0),
	(8, 9): (-1, 0),
	(9, 4): (0, -1),
	(5, 1): (0, -1),
	(7, 2): (0, -1),
	(1, 5): (0, -1),
	(3, 6): (0, -1),
	(2, 2): (1, 0),
	(8, 6): (-1, 0),
	(4, 1): (1, 0),
	(9, 7): (0, -1),
	(6, 4): (1, 0),
	(5, 4): (-1, 0),
	(7, 1): (0, -1),
	(0, 5): (0, -1),
	(1, 0): (1, 0),
	(0, 8): (0, -1),
	(3, 5): (0, -1),
	(2, 7): (1, 0),
	(8, 3): (1, 0),
	(4, 6): (0, -1),
	(9, 2): (0, -1),
	(6, 1): (0, -1),
	(5, 7): (0, -1),
	(7, 4): (1, 0),
	(0, 2): (0, -1),
	(1, 3): (0, -1),
	(4, 8): (0, -1),
	(3, 0): (1, 0),
	(2, 8): (1, 0),
	(9, 8): (0, -1),
	(8, 0): (1, 0),
	(6, 2): (0, -1),
	(5, 0): (1, 0),
	(1, 4): (0, -1),
	(3, 9): (0, -1),
	(2, 3): (0, -1),
	(1, 9): (-1, 0),
	(8, 7): (0, -1),
	(4, 2): (0, -1),
	(9, 6): (-1, 0),
	(6, 5): (1, 0),
	(5, 3): (0, -1),
	(7, 0): (1, 0),
	(6, 8): (0, -1),
	(0, 6): (0, -1),
	(1, 7): (-1, 0),
	(0, 9): (0, -1),
	(3, 4): (0, -1),
	(2, 4): (0, -1),
	(8, 4): (0, -1),
	(5, 9): (-1, 0),
	(4, 7): (0, -1),
	(9, 1): (0, -1),
	(6, 6): (0, -1),
	(5, 6): (0, -1),
	(7, 7): (0, -1),
	(0, 3): (0, -1),
	(1, 2): (1, 0),
	(4, 9): (0, -1),
	(3, 3): (0, -1),
	(2, 9): (1, 0),
	(8, 1): (0, -1),
	(4, 4): (0, -1),
	(6, 3): (0, -1),
	(0, 0): (1, 0),
	(7, 9): (-1, 0),
	(3, 8): (1, 0),
	(2, 0): (1, 0),
	(1, 8): (-1, 0),
	(8, 8): (-1, 0),
	(4, 3): (0, -1),
	(9, 5): (0, -1),
	(5, 2): (0, -1)},
	{(7, 3): (0, 1),
	(6, 9): (-1, 0),
	(0, 7): (1, 0),
	(1, 6): (0, 1),
	(3, 7): (-1, 0),
	(2, 5): (-1, 0),
	(8, 5): (-1, 0),
	(5, 8): (-1, 0),
	(4, 0): (0, 1),
	(9, 0): (-1, 0),
	(6, 7): (-1, 0),
	(5, 5): (0, 1),
	(7, 6): (-1, 0),
	(0, 4): (0, 1),
	(1, 1): (0, 1),
	(3, 2): (0, 1),
	(2, 6): (0, 1),
	(8, 2): (0, 1),
	(4, 5): (0, 1),
	(9, 3): (-1, 0),
	(6, 0): (-1, 0),
	(7, 5): (-1, 0),
	(0, 1): (0, 1),
	(3, 1): (0, 1),
	(9, 9): (-1, 0),
	(7, 8): (0, 1),
	(2, 1): (0, 1),
	(8, 9): (-1, 0),
	(9, 4): (-1, 0),
	(5, 1): (-1, 0),
	(7, 2): (0, -1),
	(1, 5): (0, 1),
	(3, 6): (0, 1),
	(2, 2): (0, 1),
	(8, 6): (-1, 0),
	(4, 1): (0, 1),
	(9, 7): (0, -1),
	(6, 4): (0, 1),
	(5, 4): (0, 1),
	(7, 1): (-1, 0),
	(0, 5): (0, 1),
	(1, 0): (0, 1),
	(0, 8): (1, 0),
	(3, 5): (0, 1),
	(2, 7): None,
	(8, 3): (0, 1),
	(4, 6): (0, 1),
	(9, 2): (0, -1),
	(6, 1): (-1, 0),
	(5, 7): (-1, 0),
	(7, 4): (0, 1),
	(0, 2): (0, 1),
	(1, 3): (0, 1),
	(4, 8): (-1, 0),
	(3, 0): (0, 1),
	(2, 8): (0, -1),
	(9, 8): (-1, 0),
	(8, 0): (-1, 0),
	(6, 2): (-1, 0),
	(5, 0): (-1, 0),
	(1, 4): (0, 1),
	(3, 9): (0, -1),
	(2, 3): (0, 1),
	(1, 9): (0, -1),
	(8, 7): (-1, 0),
	(4, 2): (0, 1),
	(9, 6): (-1, 0),
	(6, 5): (-1, 0),
	(5, 3): (0, 1),
	(7, 0): (-1, 0),
	(6, 8): (-1, 0),
	(0, 6): (0, 1),
	(1, 7): (1, 0),
	(0, 9): (1, 0),
	(3, 4): (0, 1),
	(2, 4): (-1, 0),
	(8, 4): (-1, 0),
	(5, 9): (-1, 0),
	(4, 7): (-1, 0),
	(9, 1): (0, -1),
	(6, 6): (-1, 0),
	(5, 6): (-1, 0),
	(7, 7): (-1, 0),
	(0, 3): (0, 1),
	(1, 2): (0, 1),
	(4, 9): (-1, 0),
	(3, 3): (0, 1),
	(2, 9): (0, -1),
	(8, 1): (-1, 0),
	(4, 4): (0, 1),
	(6, 3): (0, 1),
	(0, 0): (0, 1),
	(7, 9): (-1, 0),
	(3, 8): (-1, 0),
	(2, 0): (0, 1),
	(1, 8): (1, 0),
	(8, 8): (-1, 0),
	(4, 3): (0, 1),
	(9, 5): (-1, 0),
	(5, 2): (-1, 0)},
	{(7, 3): (0, -1),
	(6, 9): (-1, 0),
	(0, 7): (0, -1),
	(1, 6): (0, -1),
	(3, 7): (1, 0),
	(2, 5): (0, -1),
	(8, 5): (0, -1),
	(5, 8): (0, -1),
	(4, 0): (1, 0),
	(9, 0): (-1, 0),
	(6, 7): (0, -1),
	(5, 5): (0, -1),
	(7, 6): (0, -1),
	(0, 4): (0, -1),
	(1, 1): (1, 0),
	(3, 2): (0, -1),
	(2, 6): (0, -1),
	(8, 2): (0, -1),
	(4, 5): (0, -1),
	(9, 3): (0, -1),
	(6, 0): (1, 0),
	(7, 5): (0, -1),
	(0, 1): (1, 0),
	(3, 1): (1, 0),
	(9, 9): (-1, 0),
	(7, 8): (0, -1),
	(2, 1): (1, 0),
	(8, 9): (-1, 0),
	(9, 4): (0, -1),
	(5, 1): (1, 0),
	(7, 2): (0, -1),
	(1, 5): (0, -1),
	(3, 6): (0, -1),
	(2, 2): (1, 0),
	(8, 6): (-1, 0),
	(4, 1): (1, 0),
	(9, 7): (0, -1),
	(6, 4): (1, 0),
	(5, 4): (0, -1),
	(7, 1): (0, -1),
	(0, 5): (0, -1),
	(1, 0): (1, 0),
	(0, 8): (0, -1),
	(3, 5): (0, -1),
	(2, 7): (1, 0),
	(8, 3): (-1, 0),
	(4, 6): (0, -1),
	(9, 2): (0, -1),
	(6, 1): (0, -1),
	(5, 7): (0, -1),
	(7, 4): (0, -1),
	(0, 2): (0, -1),
	(1, 3): (0, -1),
	(4, 8): (0, -1),
	(3, 0): (1, 0),
	(2, 8): (1, 0),
	(9, 8): (-1, 0),
	(8, 0): (-1, 0),
	(6, 2): (0, -1),
	(5, 0): (1, 0),
	(1, 4): (0, -1),
	(3, 9): (0, -1),
	(2, 3): (0, -1),
	(1, 9): (1, 0),
	(8, 7): (0, -1),
	(4, 2): (0, -1),
	(9, 6): (-1, 0),
	(6, 5): (-1, 0),
	(5, 3): (0, -1),
	(7, 0): None,
	(6, 8): (0, -1),
	(0, 6): (0, -1),
	(1, 7): (-1, 0),
	(0, 9): (0, -1),
	(3, 4): (0, -1),
	(2, 4): (0, -1),
	(8, 4): (-1, 0),
	(5, 9): (-1, 0),
	(4, 7): (0, -1),
	(9, 1): (0, -1),
	(6, 6): (0, -1),
	(5, 6): (0, -1),
	(7, 7): (0, -1),
	(0, 3): (0, -1),
	(1, 2): (1, 0),
	(4, 9): (0, -1),
	(3, 3): (0, -1),
	(2, 9): (1, 0),
	(8, 1): (0, -1),
	(4, 4): (0, -1),
	(6, 3): (0, -1),
	(0, 0): (1, 0),
	(7, 9): (-1, 0),
	(3, 8): (1, 0),
	(2, 0): (1, 0),
	(1, 8): (-1, 0),
	(8, 8): (-1, 0),
	(4, 3): (0, -1),
	(9, 5): (0, -1),
	(5, 2): (0, -1)}
]


# policiesDict[0] = policies0
# policiesDict[1] = policies1
policiesDict[0] = policies1

def turn_right(direction):
	if direction == left:
		return down
	elif direction == up:
		return left
	elif direction == right:
		return up
	elif direction == down:
		return right

def turn_left(direction):
	if direction == left:
		return up
	elif direction == up:
		return right
	elif direction == right:
		return down
	elif direction == down:
		return left


# def makePolicy():
	# Make policy for each car.



def test():
	mean_score = 0
	for i in range(n):
		for j in range(10):
			score = 0
			pos = carOrigins[i]
			np.random.seed(j)
			swerve = np.random.random_sample(1000000)
			k = 0
			while (pos != carDestinations[i]):
				# policies = 2d array of turning directions for each car.
				move = policies1[i][pos]
				print(move)

				print("Policy says: ")
				if (move == left):
					print("Go Left!")
				elif (move == up):
					print("Go up!")
				elif (move == right):
					print("Go right!")
				elif (move == down):
					print("Go down!")

				print("magic number:")
				print(swerve[k])

				if swerve[k] > 0.7:
					if swerve[k] > 0.8:
						if swerve[k] > 0.9:
							move = turn_left(turn_left(move))
							print("Faulty car! Moving: ")
							if (move == left):
								print("Going Left!")
							elif (move == up):
								print("Going up!")
							elif (move == right):
								print("Going right!")
							elif (move == down):
								print("Going down!")
						else:
							move = turn_left(move) 
							print("Faulty car! Moving: ")
							if (move == left):
								print("Going Left!")
							elif (move == up):
								print("Going up!")
							elif (move == right):
								print("Going right!")
							elif (move == down):
								print("Going down!")
					else:
						move = turn_right(move)
						print("Faulty car! Moving: ")
						if (move == left):
							print("Going Left!")
						elif (move == up):
							print("Going up!")
						elif (move == right):
							print("Going right!")
						elif (move == down):
							print("Going down!")
				k += 1

				print("--> GOING %s", move)
				# print("move: ")
				# print(move)
				if (move != None):
					# got the move, so update position and add the points.
					# if move causes outside grid, reject but update score
					if (pos[0] + move[0] >= s or pos[0] + move[0] < 0 or pos[1] + move[1] >= s or pos[1] + move[1] < 0):
						pos = pos # stay in same spot
						print("Oops! Bumped against wall")
						# bumped against wall!
					else:
						pos = (pos[0] + move[0], pos[1] + move[1])
					print("newPos: ")
					print(pos)
					# pos[0] = pos[0] + move[0]
					# pos[1] = pos[1] + move[1]
					score += carMap[pos[1]][pos[0]]

				print("Current position:")
				print(pos)
				print("Destination:")
				print(carDestinations[i])
				

			# Once reached goal, add 100
			score += 100				
			mean_score += score

			print("score: ")
			print(score)
			print("=================================================")

	
	mean_score = np.floor(mean_score/10)
	# print("mean_score: ")
	return mean_score

def buildMap():
	global carMap
	# carMap = []
	carMap = [[-1 for x in range(s)] for y in range(s)] 
	# for i in range(0,s):
	# 	for j in range(0,s):
	# 		if ((str(i),str(j)) in obstacles):
	# 			carMap[i][j] = -101


	for obstacle in obstacles:
		carMap[obstacle[1]][obstacle[0]] = -101
		# print(obstacle)
	# Actually, maybe we should just keep this map to hold just obstacle info, and so it can be used for all cars.
	# Just update destination score in each iteration later.

	# update destination points
	# carMap[int()][]
	# print(carMap)


def processInput():
	global s, n, o, obstacles, carOrigins, carDestinations

	if len(sys.argv) != 1:
		print("Error with arguments")
		return -1

	with open("input.txt", "r") as f:
		lines = f.read().splitlines()
		# grid size
		s = int(lines[0])
		print(s)

		# number of cars
		n = int(lines[1])
		print(n)

		# number of obstacles
		o = int(lines[2])
		print(o)

		# obstacle locations
		for i in range(3, 3 + o):
			obstacleArr = lines[i].split(",")
			obstacleArr[0] = int(obstacleArr[0])
			obstacleArr[1] = int(obstacleArr[1])
			# print(obstacleArr)
			# print(obstacleArr)
			obstacle = tuple(obstacleArr)
			# obstacle[0] = int(obstacleArr[0])
			# obstacle[1] = int(obstacleArr[1])
			obstacles.append(obstacle)
		print("obstacles: ")
		print(obstacles)

		# car start locations
		for i in range(3 + o, 3 + o + n):

			carOriginArr = lines[i].split(",")
			carOriginArr[0] = int(carOriginArr[0])
			carOriginArr[1] = int(carOriginArr[1])
			carOrigin = tuple(carOriginArr)
			# carOriginString = lines[i].replace(',','')
			carOrigins.append(carOrigin)
		print("carOrigins: ")
		print(carOrigins)

		# car destinations
		for i in range(3 + o + n, 3 + o + n + n):

			carDestinationArr = lines[i].split(",")
			carDestinationArr[0] = int(carDestinationArr[0])
			carDestinationArr[1] = int(carDestinationArr[1])
			carDestination = tuple(carDestinationArr)

			# carDestinationString = lines[i].replace(',','')
			carDestinations.append(carDestination)
		print("car Destinations:")
		print(carDestinations)


def main():
	processInput()
	print("------------------------------------------")
	# print("n: ", n)
	# print("obstacles: ")
	# print(obstacles)
	buildMap()
	# print(carMap)
	# for x in carMap:
	    # print(*x, sep=" ")
	for row in carMap:
		print(row)
	# printInput()
	
	# print(swerve)

	# pprint.pprint(policies0)
	# pprint.pprint(policiesDict)
	finalScore = test()
	print("finalScore: ")
	print(finalScore)

	
	output = open("output.txt","w")
	output.write("%s" %finalScore)
	output.close()
	


if __name__ == "__main__":
	main()





