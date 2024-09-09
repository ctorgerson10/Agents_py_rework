import tkinter as tk
import random
from Screen import Screen
from pathlib import Path

class DrBsGui:
	def __init__(self, file:Path=None, parent=None):
		self.m = tk.Tk()
		self.m.title("Dr Bs Dungeon Crawler")
		# self.m.geometry("600x200")
		if file==None:
			self.file = findRandomLayout()
		else:
			self.file = Path(file)
		
		self.screen = Screen(self.file)

		print(self.file.absolute())

		self.m.geometry(str(self.screen.width) + "x"+str(self.screen.height))
		print(str(self.screen.width) + "x"+str(self.screen.height))

		self.setup_events()


	def setup_events(self):
		self.m.bind("<Key>", self.keyPressed)

	def keyPressed(self, keyevent):
		# print("Key pressed")
		self.screen.player.setNextMove(keyevent)
		
def loadAllFiles():
	folder = Path("DungeonLayouts")
	files = list(folder.iterdir())

	for f in files:
		if(f.is_file()):
			d = DrBsGui(f)
			d.m.mainloop()

def findRandomLayout():
	folder = Path("DungeonLayouts")
	files = list(folder.iterdir())
	f = Path(files[random.randint(0,len(files))-1])
	while f.is_dir():
		f = Path(files[random.randint(0,len(files))-1])

	return f

#Some files for testing
gui = DrBsGui(file=Path("DungeonLayouts","testMaze.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","testSearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","smallMaze.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","smallSafeSearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","smallSearch.txt"))

# # BFS should be able to complete all of these
# gui = DrBsGui(file=Path("DungeonLayouts","bigCorners.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","bigMaze.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","contoursMaze.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","mediumDottedMaze.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","mediumScaryMaze.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","openMaze.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","trappedClassic.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","trickySearch.txt"))

		
# # Two more for us to try, but probably not BFS
# gui = DrBsGui(file=Path("DungeonLayouts","oddSearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","smallClassic.txt"))

# # If you want, these should also be a go for BFS
# gui = DrBsGui(file=Path("DungeonLayouts","capsuleClassic.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","greedySearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","mediumCorners.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","mediumMaze.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","mediumSafeSearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","minimaxClassic.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","testClassic.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","tinyCorners.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","tinyMaze.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","tinySearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","tinySafeSearch.txt"))

# #Maybe - but not BFS, DFS can do all of these, probably not uniform cost
# gui = DrBsGui(file=Path("DungeonLayouts","bigSafeSearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","bigSearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","boxSearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","contestClassic.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","mediumClassic.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","mediumSearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","openClassic.txt"))		
# gui = DrBsGui(file=Path("DungeonLayouts","openSearch.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","originalClassic.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","powerClassic.txt"))
# gui = DrBsGui(file=Path("DungeonLayouts","trickyClassic.txt"))

gui.m.mainloop()
