import numpy as np
import game2048
import valueFunction
import sys, os
import random


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

Players = Enum(["AI", "COMPUTER"])

class miniMax:

	def __init__(self, grid):
		self.grid = grid
		self.result = {'bestscore': 0, 'bestdirection': None}

	def find_best_move(self, grid, depth):		
		r = {}
		#result = alphabeta(grid, depth, -sys.maxint-1, sys.maxint, Players.AI)
		r = self.minimax(grid, depth, Players.AI)
		

		if r['bestdirection'] == 0:
			return 'w'
		elif r['bestdirection'] == 1:
			return 'd'
		elif r['bestdirection'] == 2:
			return 's'
		elif r['bestdirection'] == 3:
			return 'a'
		# 0,w:up    1,d:right     2,s:down    3,a:left

	def minimax(self, grid, depth, player):

		v = valueFunction.ValueFunction()
		s = game2048.in2048()

		actions = s.getActions()

		#result = {'bestscore': 0, 'bestdirection': None}   # result[0] is bestscore, result[1] is bestdirection

		if depth == 0 or not actions:  # check whether the game is over
			bestscore = v.get(grid) 
			self.result['bestscore'] = bestscore # eveluate the grid by eveluation fucntion

			#print result
			return  self.result

		elif player == Players.AI :
			bestscore = -sys.maxint - 1
			for i in range(len(actions)):
				op = actions[i]
				newgrid = s.states[op][1]
				
				points = v.get(newgrid)
				

				currentScore = {}
				currentScore = self.minimax(newgrid, depth-1, Players.COMPUTER)  
				print currentScore

				if currentScore['bestscore'] > bestscore:
					bestscore = currentScore['bestscore']
					bestDirection = actions[i]
					#print bestDirection
			self.result['bestscore'] = bestscore
			self.result['bestdirection'] = bestDirection
			#print result
			return self.result

		else:
			#print ("EI")
			bestscore1 = sys.maxint
			newgrid1 = s.addRandomTile(grid)
			newgrid2 = s.addRandomTile(grid)
			newgrid3 = s.addRandomTile(grid) 
			newgrid = [newgrid1, newgrid2, newgrid3]
			
			for j in range(3):
				points = v.get(newgrid[j])
				#print points
				currentScore1 = {}
				currentScore1 = self.minimax(newgrid[j], depth-1, Players.AI)
				#print currentScore1
				if currentScore1['bestscore'] < bestscore1:
						bestscore1 = currentScore1['bestscore']
						self.result['bestscore'] = bestscore1
			#print ("GI")
			return self.result

	# def alphabeta(self, grid, depth, alpha, beta, player):
	# 	v = valueFunction.ValueFunction()
	# 	s = in2048()

	# 	actions = s.getActions()
	# 	#moves = s.move(actions)
	# 	result = {'bestscore': 0, 'bestdirection': None}

	# 	if depth == 0 or not actions:
	# 		bestscore = v.get(self.grid)
	# 		return result.append(bestscore),result.append(None)

	# 	elif player == Players.AI:
	# 		bestscore = -sys.maxint - 1
	# 		for j in actions:
	# 			newgrid = s.move(i, 3)[1]

	# 			points = v.get(newgrid)
	# 			if points == 0 and newgrid == self.grid:
	# 				continue

	# 			currentScore = self.alphabeta(newgrid, depth-1, alpha, beta, Players.COMPUTER)[0] + points
	# 			if currentScore > alpha:
	# 				alpha = currentScore
	# 			if beta <= alpha:
	# 				break                      # beta cutoff
	# 		bestscore = alpha
	# 		bestDirection = actions[j]
	# 		return result['bestscore'] = bestscore, result['bestdirection'] = bestDirection

	# 	else:
	# 		bestscore = sys.maxint
	# 		freeCells = s.availableCell(self.grid)

	# 		if freeCells.size <= 3:
	# 			for cell in freeCells:
	# 				newgrid = in2048(self.grid)
	# 				newgrid1 = s.addRandomTile(newgrid)
	# 				points = v.get(newgrid1)
	# 				currentScore = alphabeta(newgrid1, depth-1, alpha, beta, Players.AI)[0] + points

	# 				if currentScore < beta:
	# 					beta = currentScore
	# 				if beta <= alpha:
	# 					break                #alpha cutoff

	# 			bestscore = beta
	# 			return result['bestscore'] = bestscore

	# 		else:
	# 			for cell in random.sample(freeCells, 3):          # keep three samples
	# 				newgrid = in2048(self.grid)
	# 				newgrid2 = s.addRandomTile(newgrid)
	# 				points = v.get(newgrid2)
	# 				currentScore = alphabeta(newgrid2, depth-1, alpha, beta, Players.COMPUTER)[0] + points

	# 				if currentScore < beta:
	# 					beta = currentScore
	# 				if beta <= alpha:
	# 					break            #alpha cutoff

	# 			bestscore = beta
	# 			return result['bestscore'] = bestscore
