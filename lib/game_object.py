from lib.agent_action import AgentAction
from lib.agent_brain import AgentBrain
import tkinter as tk
import random
from pathlib import Path


class GameObject:
    def __init__(self, col: float, row: float, i: tk.PhotoImage, tileSize: int, imageWidth: int = None,
                 imageHeight: int = None):
        self.colOnGraphics = col  #x
        self.rowOnGraphics = row  #y
        self.image = i
        self.tileSize = tileSize
        self.brain = AgentBrain()
        self.tileSize = tileSize
        self.redraw = True
        # self.brain = new AgentBrain();

        self.imageWidth = imageWidth
        if self.imageWidth == None or self.imageHeight == None:
            if type(i) != list:
                the_image_height = i.tk.getint(i.tk.call('image', 'height', i.name))
                the_image_width = i.tk.getint(i.tk.call('image', 'width', i.name))
                if (tileSize == 16):
                    self.image = self.image.subsample(2, 2)
                self.imageHeight = tileSize
                self.imageWidth = tileSize
            else:
                the_image_height = i[0].tk.getint(i[0].tk.call('image', 'height', i[0].name))
                the_image_width = i[0].tk.getint(i[0].tk.call('image', 'width', i[0].name))
                if (tileSize == 16):
                    for j in range(len(i)):
                        i[j] = i[j].subsample(2, 2)
                self.imageHeight = tileSize
                self.imageWidth = tileSize

    def getRowLocation(self):
        return int(self.rowOnGraphics // self.tileSize)

    def getColLocation(self):
        return self.colOnGraphics // self.tileSize

    def setRowLocation(self, row: int):
        self.rowOnGraphics = row * self.tileSize

    def setColLocation(self, col: int):
        self.colOnGraphics = col * self.tileSize

    def drawTheImage(self, parent):
        if (self.image != None):
            # print("drawing at ",self.colOnGraphics,self.rowOnGraphics)
            if (type(self.image) != list):
                if (self.redraw):
                    self.redraw = False
                    parent.create_image(self.colOnGraphics, self.rowOnGraphics, image=self.image, anchor=tk.NW)
            else:
                if (self.redraw):
                    self.redraw = False
                    for i in self.image:
                        parent.create_image(self.colOnGraphics, self.rowOnGraphics, image=i, anchor=tk.NW)

    def setNextMove(self, keyevent):
        keychar = keyevent.char
        if (keychar == ""):
            keychar = keyevent.keysym
        # print("Key Event '" + str(keyevent) +"'")
        # print("Key char '" + keychar +"'")

        up = ["w", "W", "Up"]
        down = ["s", "S", "Down"]
        left = ["a", "A", "Left"]
        right = ["d", "D", "Right"]
        victory = ["v", "V"]
        pickup = [" "]

        if keychar in right:
            self.brain.addNextMove(AgentAction.moveRight)
        elif keychar in left:
            self.brain.addNextMove(AgentAction.moveLeft)
        elif keychar in up:
            self.brain.addNextMove(AgentAction.moveUp)
        elif keychar in down:
            self.brain.addNextMove(AgentAction.moveDown)
        elif keychar in victory:
            self.brain.addNextMove(AgentAction.declareVictory)
        elif keychar in pickup:
            self.brain.addNextMove(AgentAction.pickupSomething)
        else:
            print("Unknown key event " + str(keyevent))

    def getMove(self) -> AgentAction:
        return self.brain.getNextMove()

    def search(self, theMap: list[list[str]]):
        self.brain.search(theMap)
