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
policies = []

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

maps = {}


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


class MDP:
	def __init__(self, actions, states, transModel, rewards, gamma):
		self.states = states
		self.actions = actions
		self.transModel = transModel
		self.rewards = rewards
		self.gamma = gamma

	def myPrint(self):
		print("------------------------------------")
		
		print("Actions:")
		print(self.actions)
		print("")
		print("States:")
		print(self.states)
		print("")
		# print("Transition Model:")
		# pprint.pprint(self.transModel)
		print("")
		print("Rewards:")
		print(self.rewards)
		print("")
		print("Gamma:")
		print(self.gamma)

		print("------------------------------------")

def findBestActionUtility(s, mdp, U, z):
	utilityList = []
	if (s == carDestinations[z]):
		# print(U[s])
		return 0
	for a in mdp.actions:
		# get all pairs for this specific action (should be 4 pairs)
		pairs = mdp.transModel[s][a]
		maxAction = None
		actionUtility = 0
		for pair in pairs:
			resultingState = pair[0]
			prob = pair[1]
			# print(prob)
			# add these 
			actionUtility += prob * U[resultingState]
		utilityList.append(actionUtility)

	maxUtility = max(utilityList)
	return maxUtility
	# print(utilityList)
	# print(maxUtility)

def value_iteration(mdp, maxError, z):
	Uprime = dict([(s, 0) for s in mdp.states])
	# for obstacle in obstacles
	# pprint.pprint(U1)
	R, T, gamma = mdp.rewards, mdp.transModel, mdp.gamma
	# pprint.pprint(U1)
	# return []
	done = False
	while not done:
		U = Uprime.copy()
		delta = 0
		for s in mdp.states:
			best_action_utility = findBestActionUtility(s,mdp,U, z)

			Uprime[s] = R[s] + gamma * best_action_utility
			# if (s in obstacles):
				# print(Uprime[s])
			# Uprime[s] = R[s] + gamma * np.max([sum([p * U[s1] for (s1,p) in T[s][a] ]) for a in mdp.actions])
			# delta = max(delta, abs(Uprime[s] - U[s]))


		if abs(Uprime[s] - U[s]) > delta:
			delta = abs(Uprime[s] - U[s])

		if (delta < (maxError * (1-gamma) / gamma)):
			return U

		# cutoff = maxError * (1 - gamma) / gamma
		# # print("delta")a
		# # print(delta)
		# # print("cutoff")
		# # print(cutoff)
		
		# if (delta < cutoff):
		# 	return U


def test():
	orientations = NORTH, SOUTH, EAST, WEST = [(1, 0), (0, -1), (-1, 0), (0, 1)]
	turns = LEFT, RIGHT = (+1, -1)
	output = open("output.txt","w")
	

	def turn_heading(heading, inc, headings=orientations):
		return headings[(headings.index(heading) + inc) % len(headings)]

	def turn_right(heading):
		return turn_heading(heading, RIGHT)

	def turn_left(heading):
		return turn_heading(heading, LEFT)

	for i in range(n):
		masterScores = []
		mean_score = 0
		for j in range(10):
			# print("%s~~~~~~~~~~~~~~~~~~~~~~~" %j)
			score = 0
			pos = carOrigins[i]
			np.random.seed(j)
			swerve = np.random.random_sample(1000000) 
			k = 0
			while pos != carDestinations[i]:
				move = policies[i][pos]
				if swerve[k] > 0.7:
					if swerve[k] > 0.8:
						if swerve[k] > 0.9:
							move = turn_right(turn_right(move)) 
						else:
							move = turn_right(move)
					else:
						move = turn_left(move)
				
				# print("MOVE: %s" %(move,)),
				if (move != None):
					# got the move, so update position and add the points.
					# if move causes outside grid, reject but update score
					if (pos[0] + move[0] >= s or pos[0] + move[0] < 0 or pos[1] + move[1] >= s or pos[1] + move[1] < 0):
						pos = pos # stay in same spot
					else:
						pos = (pos[0] + move[0], pos[1] + move[1])
					score += carMap[pos[1]][pos[0]]
					
					# if (pos == carDestinations[i]):
					# 	print("		VALUE GAINED: %s" %(carMap[pos[1]][pos[0]] + 100)),
					# else:
					# 	print("		VALUE GAINED: %s" %carMap[pos[1]][pos[0]]),
					# print("		SWERVE VALUE: %s" %swerve[k])
				k += 1
			score += 100.0
			masterScores.append(score)
			# print("SCORE: %s" %masterScores)
			mean_score += score
		mean_score = (mean_score/10.0)
		# print("AVERAGE SCORE: %s" %mean_score)
		mean_score_floored = np.floor(mean_score)
		# print("FLOORED AVERAGE SCORE: %s" %mean_score_floored)
		output.write("%s\n" %int(mean_score))
	output.close()



def test2():
	
	output = open("output.txt","w")
	for i in range(n):
		mean_score = 0
		for j in range(10):
			score = 0
			pos = carOrigins[i]
			np.random.seed(j)
			swerve = np.random.random_sample(1000000)
			k = 0
			# print(policies[0])
			while (pos != carDestinations[i]):
				# policies = 2d array of turning directions for each car.
				move = policies[i][pos]
				# print(move)

				# print("Policy says: ")
				# if (move == left):
				# 	print("Go Left!")
				# elif (move == up):
				# 	print("Go up!")
				# elif (move == right):
				# 	print("Go right!")
				# elif (move == down):
				# 	print("Go down!")

				# print("magic number:")
				# print(swerve[k])

				if swerve[k] > 0.7:
					if swerve[k] > 0.8:
						if swerve[k] > 0.9:
							move = turn_left(turn_left(move))
							# print("Faulty car! Moving: ")
							# if (move == left):
							# 	print("Going Left!")
							# elif (move == up):
							# 	print("Going up!")
							# elif (move == right):
							# 	print("Going right!")
							# elif (move == down):
							# 	print("Going down!")
						else:
							move = turn_left(move) 
							# print("Faulty car! Moving: ")
							# if (move == left):
							# 	print("Going Left!")
							# elif (move == up):
							# 	print("Going up!")
							# elif (move == right):
							# 	print("Going right!")
							# elif (move == down):
							# 	print("Going down!")
					else:
						move = turn_right(move)
						# print("Faulty car! Moving: ")
						# if (move == left):
						# 	print("Going Left!")
						# elif (move == up):
						# 	print("Going up!")
						# elif (move == right):
						# 	print("Going right!")
						# elif (move == down):
						# 	print("Going down!")
				k += 1

				# print("--> GOING %s", move)
				# print("move: ")
				# print(move)
				if (move != None):
					# got the move, so update position and add the points.
					# if move causes outside grid, reject but update score
					if (pos[0] + move[0] >= s or pos[0] + move[0] < 0 or pos[1] + move[1] >= s or pos[1] + move[1] < 0):
						pos = pos # stay in same spot
						# print("Oops! Bumped against wall")
						# bumped against wall!
					else:
						pos = (pos[0] + move[0], pos[1] + move[1])
					# print("newPos: ")
					# print(pos)
					# pos[0] = pos[0] + move[0]
					# pos[1] = pos[1] + move[1]
					score += carMap[pos[1]][pos[0]]

				# print("Current position:")
				# print(pos)
				# print("Destination:")
				# print(carDestinations[i])
				

			# Once reached goal, add 100
			score += 100				
			mean_score += score

			# print("score: ")
			# print(score)
			# print("=================================================")
		mean_score = int(np.floor(mean_score/10))
		output.write("%s\n" %mean_score)

	
	output.close()

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
		# print(s)

		# number of cars
		n = int(lines[1])
		# print(n)

		# number of obstacles
		o = int(lines[2])
		# print(o)

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
		# print("obstacles: ")
		# print(obstacles)

		# car start locations
		for i in range(3 + o, 3 + o + n):

			carOriginArr = lines[i].split(",")
			carOriginArr[0] = int(carOriginArr[0])
			carOriginArr[1] = int(carOriginArr[1])
			carOrigin = tuple(carOriginArr)
			# carOriginString = lines[i].replace(',','')
			carOrigins.append(carOrigin)
		# print("carOrigins: ")
		# print(carOrigins)

		# car destinations
		for i in range(3 + o + n, 3 + o + n + n):

			carDestinationArr = lines[i].split(",")
			carDestinationArr[0] = int(carDestinationArr[0])
			carDestinationArr[1] = int(carDestinationArr[1])
			carDestination = tuple(carDestinationArr)

			# carDestinationString = lines[i].replace(',','')
			carDestinations.append(carDestination)
		# print("car Destinations:")
		# print(carDestinations)

# def expected_utility(a, s, U, mdp):
#     # "The expected utility of doing a in state s, according to the MDP and U."
#     return sum([p * U[s1] for (s1, p) in mdp.T[s][a]])

# def best_policy(mdp, U):
#     """Given an MDP and a utility function U, determine the best policy,
#     as a mapping from state to action. (Equation 17.4)"""
#     pi = {}
#     for s in mdp.states:

#     	currentState = s



#         pi[s] = np.argmax(mdp.actions, lambda a:expected_utility(a, s, U, mdp))
#     return pi
def findOptimalPolicy(myMdp,V):
	policy = {}
	for state in (myMdp.states):

		U = V.copy()
		A = dict([(a, 0) for a in myMdp.actions])
		# print(A)

		for a in myMdp.actions:

			for pair in myMdp.transModel[state][a]:
				resultingState = pair[0]
				prob = pair[1]
				# print(resultingState)
				# print(prob)

				A[a] += prob * (myMdp.rewards[state] + myMdp.gamma * V[resultingState])
		bestActionVal = -99999999
		priorityActionMap = {up: 4, down: 3, right: 2, left: 1}
		# print(A)
		# print(state)
		for action, actionVal in A.iteritems():
			if (actionVal > bestActionVal):
				bestActionVal = actionVal
				bestAction = action
			elif (actionVal == bestActionVal):
				if (priorityActionMap[action] > priorityActionMap[bestAction]):
					bestAction = action
					bestActionVal = actionVal

		# print(bestAction)
		policy[state] = bestAction

	return policy

def main():
	# global policies
	processInput()
	# print("------------------------------------------")
	buildMap()
	# pprint.pprint(carMap)
	# for row in carMap:
	# 	print(row)
	finalScore = 0
	# finalScore = test()
	# policies = {}


	# def __init__(self, actions, states, transModel, rewards, gamma):
	# actions
	for z in range(n):
		actions = [up, down, left, right]
		# states
		states = []
		for i in range(s):
			for j in range(s):
				states.append((j,i))
		# transition model
		transModel = {}
		for i in range(s*s):
			curState = states[i]
			stateActions = {}
			for action in actions:
				possibleResultStates = []
				for action2 in actions:
					# statePair = [0,0]
					resultingState = tuple(map(sum, zip(curState,action2)))
					if (resultingState[0] >= s or resultingState[0] < 0 or resultingState[1] >= s or resultingState[1] < 0):
						resultingState = curState
					prob = 0
					if action2 == action:
						prob = 0.7
					else:
						prob = 0.1
					statePair = (resultingState, prob)
					possibleResultStates.append(statePair)

				stateActions[action] = possibleResultStates

			transModel[curState] = stateActions
		# pprint.pprint(transModel)
		# rewards
		rewards = {}
		for i in range(s*s):
			curState = states[i]
			if (curState in obstacles):
				rewards[curState] = -101
			elif (curState == carDestinations[z]):
				rewards[curState] = 99
			else:
				rewards[curState] = -1
		# gamma
		gamma = 0.9
		myMdp = MDP(actions, states, transModel, rewards, gamma)
		# pprint.pprint(myMdp)
		# myMdp.myPrint()
		maxError = 0.1
		V = value_iteration(myMdp, maxError, z)
		# pprint.pprint(V)
		policy = findOptimalPolicy(myMdp,V)
		policies.append(policy)

	# pprint.pprint(policies)
	# pprint.pprint(policies)
	test()

	# pprint.pprint(policy)
	# print("finalScore: ")
	# print(finalScore)
	
	


if __name__ == "__main__":
	main()





