from AgentAction import AgentAction
from Variables import Variables

class GameState:

	#This constructor assumes that there is an 'S' somewhere on the map and the game is just starting
	#i.e., no parent node, and no distance
	def __init__(self, map, parent_state = None, newX = -1, newY = -1):
		GameState.numNodesCreated+=1 #One more node created

		self.map = None

		#x and y are the locations of the character on the map
		self.row = 0
		self.col = 0
		#Action will ultimately be the action we take - Note: Do not create "new" ones, just use the existing static ones
		self.action = None

		#For now, we will say that two states are the same if they have the same string representation
		#Currently build like "x y mapCharactersHere"
		self.stringRepresentationOfState = None #We may need to do lazy instantiation on this, if it is slow

		#Parent is the GameState that generated this one
		if parent_state is None:
			self.parent = None
			#Distance is the current distance the character traveled to get to this location, not how far remaining
			self.currentDistance = 0
			newX = -1
			newY = -1
			self.map = []
			for i in range(len(map)):
				self.map.append([])
				for j in range (len(map[0])):
					#Copy things over
					self.map[i].append(map[i][j])

					#emove the player from the map
					if self.map[i][j] == Variables.S_PLAYER_AND_MISSING_GOLD:
						newX = i
						newY = j
						self.map[i][j] = Variables.S_MISSING_GOLD #Remove the player
					elif self.map[i][j] == Variables.S_PLAYER_AND_GOLD:
						newX = i
						newY = j
						self.map[i][j] = Variables.S_GOLD #Remove the player from the map
					elif self.map[i][j] == Variables.S_PLAYER:
						newX = i
						newY = j
						self.map[i][j] = Variables.S_GROUND #Remove the player from the map
					else:
						#things are fine
						pass

				self.row = newX
				self.col = newY
		else:
			self.parent = parent_state
			self.currentDistance = parent_state.currentDistance+1
			self.row = newX
			self.col = newY
			self.map = []
			for i in range(len(map)):
				self.map.append([])
				for j in range (len(map[0])):
					self.map[i].append(map[i][j])

		self.rebuildStringRepresentation()


	def __str__(self):		
		return self.stringRepresentationOfState
	
	def __hash__(self) -> int:
		return self.stringRepresentationOfState.__hash__()

	#TODO - you can leave this for now, but when we are implementing a priority queue, we will likely have to change this
	#To compare estimated distance from goal
	def __lt__ (self, other):
		return self.stringRepresentationOfState < other.stringRepresentationOfState
	def __gt__ (self, other):
		return other.__lt__(self)
	def __eq__ (self, other):
		return self.stringRepresentationOfState == other.stringRepresentationOfState and self.stringRepresentationOfState == other.stringRepresentationOfState
	def __ne__ (self, other):
		return not self.__eq__(other)	

	def changeGoldToGround(self, row, col):
		if row >= 0 and row <= len(self.map) and col >= 0 and col < len(self.map[0]) and self.map[row][col] == Variables.S_GOLD:
			self.map[row][col] = Variables.S_GROUND
			self.rebuildStringRepresentation()
	
	def changeMissingGoldToGold(self, row, col):
		if row >= 0 and row <= len(self.map) and col >= 0 and col < len(self.map[0]) and self.map[row][col] == Variables.S_MISSING_GOLD:
			self.map[row][col] = Variables.S_GOLD
			self.rebuildStringRepresentation()

	def rebuildStringRepresentation(self):
		sb = ""
		for i in range(0,len(self.map)):
			for j in range(0,len(self.map[i])):
				#Patch if necessary
				if self.map[i][j] == Variables.S_MISSING_GOLD:
					sb = sb+Variables.S_GROUND #Keep the missing gold, but put ground in our state
				else:
					sb = sb+self.map[i][j]
		self.stringRepresentationOfState = str(self.row) + " " + str(self.col) + " " + sb
	

	def printMaze(self):
		for i in len(map):
			for j in len(map[i]):
				if i == self.row and j == self.col:
					if map[i][j] == Variables.S_GOLD:
						print (Variables.S_PLAYER_AND_GOLD, end="")
					else:
						print(Variables.S_PLAYER, end="")
				else:
					print(map[i][j], end="")
			print("")

	def getAllActions(self):
		if self.parent == None:
			moves = []
			if self.action != None:
				moves.append(self.action)
			return moves
		else:
			moves = self.parent.getAllActions()
			moves.append(self.action)
			return moves

	def isGoalState(self):
		#TODO
		return True

	def getNextStates(self):
		#TODO
		return None

	@staticmethod
	def search(problem):
		#TODO, change this next line as we introduce different types of search
		return GameState.breadthFirstSearch(problem)

	@staticmethod
	def breadthFirstSearch(problem):
		#Some static variables so that we can determine how "hard" problems are
		GameState.numNodesExplored = 0
		GameState.numNodesCreated = 0

		node = GameState(problem) #Essentially the second line of the book's BFS
		if(node.isGoalState()): #Essentially the start of line 3 of the book's BFS
			node.action = AgentAction.declareVictory #We don't have to do anything
			return node.getAllActions() #Just the single thing, but this is an example for later


		#Create the frontier queue, and reached hash
		frontier = []
		reached = set()

		#Add the first node to the hash
		reached.add(node)

		#TODO - create the rest of the BFS function

#		node = frontier.pop(0) #retrieve and remove

		GameState.numNodesExplored+=1 #we are now ready to "explore" the starting node

		#Print this at the end, so we know how "hard" the problem was
		print("Number of nodes explored =", GameState.numNodesExplored)
		print("Number of nodes created =",  GameState.numNodesCreated)

		#return the goalNode.getAllActions() if you find a goal node
		
		return None

GameState.numNodesExplored = 0
GameState.numNodesCreated = 0
