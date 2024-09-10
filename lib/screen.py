import tkinter as tk
import random
from pathlib import Path
from lib.game_object import GameObject
from lib.agent_action import AgentAction
from lib.variables import Variables

from lib.game_state_reversed import GameStateReversed

class Screen (tk.Canvas):

	def __init__(self, filename:Path):
		super(Screen, self).__init__()

		self.theMap = []
		input = open(filename)
		# print("Working on " + str(filename.absolute()))
		contents = []

		for line in input:
			contents.append(line)
		
		self.rows = len(contents)
		self.cols = len(contents[0])-1#newline at the end of each row
		# print("with",self.rows,self.cols)

		for i in range(0,self.rows):
			self.theMap.append([])
			for j in range(0, self.cols): 
				self.theMap[i].append(contents[i][j])

		input.close()

		print(self.theMap)

		# maps = GameStateReversed.createInitialGameStates(self.theMap)
		# for i in range(0,len(maps)):
		# 	print(maps[i])

		self.mapName = filename.name
		self.mapName = self.mapName[0:self.mapName.find(".")]
		self.setupInitialVariables()

		self.pack(fill="both", expand=True)
		self.draw_full_background()
		self.paint()


	def setupInitialVariables(self):

		# just in case things don't work so well with the map
		self.width = 10*Variables.tileSize
		self.height = 10*Variables.tileSize

		# print("Key Listener")
		# print("\tawsd or arrows to move")
		# print("\tspacebar to pickup gold")
		# print("\tv to declare victory")

		self.enemys = []
		self.gold = []
		self.elixers = []

		self.numActions = 0
		self.playerDeclaresVictory = False
		self.numEnemyHits = 0

		self.map = [[None] * self.cols for i in range(self.rows)]
		self.screen = [[None] * self.cols for i in range(self.rows)]

		# Select the images to use for this run
		self.wall = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","dungeon","wall"))
		self.ground = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","dungeon","floor"))
		if Variables.tileSize == 16:
			self.wall = self.wall.subsample(2,2)
			self.ground = self.ground.subsample(2,2)

		# print("again", self.rows, self.cols)
		# print(self.screen)

		for i in range(0, self.rows):
			# print("row",i)
			for j in range(0,self.cols):
				# print("col",j)
				if(self.theMap[i][j]==Variables.S_WALL):
					self.screen[i][j] = self.wall
				elif(self.theMap[i][j]==Variables.S_GROUND):
					self.screen[i][j] = self.ground
				elif(self.theMap[i][j]==Variables.S_PLAYER):
					self.screen[i][j] = self.ground
					self.loadPlayerImage(j,i)
				elif(self.theMap[i][j]==Variables.S_PLAYER_AND_GOLD):
					self.screen[i][j] = self.ground
					self.coin = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","item","gold"))
					self.gold.append(GameObject(j*Variables.tileSize,i*Variables.tileSize,coin,Variables.tileSize))
					self.loadPlayerImage(j,i)
				elif(self.theMap[i][j]==Variables.S_GOLD):
					#put the gold on the ground
					coin = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","item","gold"))
					self.gold.append(GameObject(j*Variables.tileSize,i*Variables.tileSize,coin,Variables.tileSize))
					self.screen[i][j] = self.ground
				elif(self.theMap[i][j]==Variables.S_ENEMY):
					enemy = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","monster"))
					self.enemys.append(GameObject(j*Variables.tileSize,i*Variables.tileSize,enemy,Variables.tileSize))
					self.screen[i][j] = self.ground
				elif(self.theMap[i][j]==Variables.S_ELIXER):
					elixer = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","item","potion"))
					self.elixers.append(GameObject(j*Variables.tileSize,i*Variables.tileSize,elixer,Variables.tileSize))
					self.screen[i][j] = self.ground
				else:
					print("Unhandled case: '" + self.theMap[i][j]+"'")
					raise AttributeError()
				self.map[i][j] = self.theMap[i][j]

		self.startingGold = len(self.gold)
		
		self.player.search(self.map)

		# self.setSize(self.cols*Variables.tileSize,self.rows*Variables.tileSize)
		self.width = self.cols*Variables.tileSize
		self.height = self.rows*Variables.tileSize


	def loadPlayerImage(self, col:int, row:int):
		playerImage = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","player","base"))
		playerImage = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","player","cloak"),bottomStartingImage=playerImage)
		playerImage = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","player","boots"),bottomStartingImage=playerImage)
		playerImage = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","player","gloves"),bottomStartingImage=playerImage)
		playerImage = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","player","draconic_head"),bottomStartingImage=playerImage)
		playerImage = self.findRandomImage(Path("images","Dungeon Crawl Stone Soup Full","player","draconic_wing"),bottomStartingImage=playerImage)
		self.player = GameObject(col*Variables.tileSize,row*Variables.tileSize,playerImage,Variables.tileSize)
	

	def findRandomImage(self, foldername:Path, bottomStartingImage = None):
		folder = foldername
		files = list(folder.iterdir())
		num = random.randint(0,len(files)-1) #both inclusive
		f = files[num]
		while f.is_dir(): #2 folders in that array
			f = files[random.randint(0,len(files)-1)]

		# print(f.absolute())
		image = tk.PhotoImage(file=f.absolute())
		if bottomStartingImage:
			if(type(bottomStartingImage) != list):
				return [bottomStartingImage,image]
			else:
				bottomStartingImage.append(image)
				return bottomStartingImage
		return image


	def isValidMove(self, newRow:int, newCol:int):
		# print("Looking at spot " + str(newRow) + " " + str(newCol))
		if 0 <= newRow and 0 <= newCol and newRow < len(self.screen) and newCol < len(self.screen[0]):
			#print("In bounds")
			if self.screen[newRow][newCol] == self.ground:
				#print("Found ground in that spot")
				return True
			else:
				#print("Didn't find a ground tile")
				if self.screen[newRow][newCol] == self.wall:
					#print("Found a wall")
					pass
		else:
			print("Out of bounds")

		return False

	def move(self, g:GameObject):
		action = g.getMove()
		if action == None:
			return
		
		col = g.getColLocation()
		row = g.getRowLocation()

		if action == AgentAction.declareVictory:
			self.playerDeclaresVictory = True

		elif action == AgentAction.pickupSomething:
			self.player.redraw = True
			for go in self.gold:
				if go.getColLocation() == col and go.getRowLocation() == row:
					self.gold.remove(go)
					#re-draw that square
					self.create_image(col*Variables.tileSize, row*Variables.tileSize,image=self.screen[row][col], anchor=tk.NW)
					break #assume only 1 gold can be picked up at a time

			for go in self.elixers:
				if go.getColLocation() == col and go.getRowLocation() == row:
					self.elixers.remove(go)
					#re-draw that square
					self.create_image(col*Variables.tileSize, row*Variables.tileSize,image=self.screen[row][col], anchor=tk.NW)
					break  #assume only 1 elixer can be picked up at a time

		elif action == AgentAction.moveRight:
			if self.isValidMove(row,col+1):
				self.update_objects_that_need_to_redraw(row,col)
				g.setColLocation(col+1)
		elif action == AgentAction.moveLeft:
			if self.isValidMove(row,col-1):
				self.update_objects_that_need_to_redraw(row,col)
				g.setColLocation(col-1)
		elif action == AgentAction.moveUp:
			if self.isValidMove(row-1,col):
				self.update_objects_that_need_to_redraw(row,col)
				g.setRowLocation(row-1)
		elif action == AgentAction.moveDown:
			if self.isValidMove(row+1,col):
				self.update_objects_that_need_to_redraw(row,col)
				g.setRowLocation(row+1)
		elif action == AgentAction.doNothing:
			pass
		else:
			print("Unhandled action " + str(action))

		if action.isAnAction:
			self.numActions+=1

	def update_objects_that_need_to_redraw(self, row:int, col:int):
		self.player.redraw = True
		self.create_image(col*Variables.tileSize, row*Variables.tileSize,image=self.screen[row][col], anchor=tk.NW)
		# for i in range(0,self.rows):
		# 	for j in range(0,self.cols):
		# 		self.create_image(j*Variables.tileSize, i*Variables.tileSize,image=self.screen[i][j], anchor=tk.NW)
		for g in self.gold:
			if g.getColLocation() == col and g.getRowLocation() == row:
				g.redraw = True
		for g in self.elixers:
			if g.getColLocation() == col and g.getRowLocation() == row:
				g.redraw = True
		for g in self.enemys:
			if g.getColLocation() == col and g.getRowLocation() == row:
				g.redraw = True

	def paint(self):
		
		if(self.playerDeclaresVictory):
			print("Map: " + self.mapName)
			print("Gold Remaining " + str(len(self.gold)) + " of " + str(self.startingGold))
			print("Total Actions: " + str(self.numActions))
			print("Enemy Hits: " + str(self.numEnemyHits))
			self.after(Variables.SLEEP_TIME*3,self.exit_game)
			return
		else:
			self.move(self.player)

		#draw the gold
		for g in self.gold:
			g.drawTheImage(self)

		#draw the elixers
		for g in self.elixers:
			g.drawTheImage(self)

		#draw the enemies
		for g in self.enemys:
			g.drawTheImage(self)
			if(self.sameSquare(self.player,g)):
				self.numEnemyHits+=1
				print("Hit an enemy")

		self.player.drawTheImage(self)

		self.after(Variables.SLEEP_TIME,self.paint)


	def sameSquare(self, a:GameObject, b:GameObject):
		if a.getColLocation() == b.getColLocation() and a.getRowLocation() == b.getRowLocation():
			return True
		return False
	
	def draw_full_background(self):
		if(self.screen != None):
			for i in range(0,self.rows):
				for j in range(0,self.cols):
					self.create_image(j*Variables.tileSize, i*Variables.tileSize,image=self.screen[i][j], anchor=tk.NW)
					# print("Location " + str(j*Variables.tileSize) + " " + str(i*Variables.tileSize))

	def exit_game(self):
		exit(0)
