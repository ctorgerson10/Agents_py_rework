from lib.agent_action import AgentAction
from lib.agent_brain import AgentBrain
import tkinter as tk
import random
from pathlib import Path


class GameObject:
    def __init__(self, col: float, row: float, i: tk.PhotoImage, tile_size: int, image_width: int = None,
                 image_height: int = None):
        self.col_on_graphics = col  # x
        self.row_on_graphics = row  # y
        self.image = i
        self.tile_size = tile_size
        self.brain = AgentBrain()
        self.redraw = True

        self.image_width = image_width
        self.image_height = None
        if self.image_width is None or self.image_height is None:
            if type(i) is not list:
                the_image_height = i.tk.getint(i.tk.call('image', 'height', i.name))
                the_image_width = i.tk.getint(i.tk.call('image', 'width', i.name))
                if tile_size == 16:
                    self.image = self.image.subsample(2)
                self.image_height = tile_size
                self.image_width = tile_size
            else:
                the_image_height = i[0].tk.getint(i[0].tk.call('image', 'height', i[0].name))
                the_image_width = i[0].tk.getint(i[0].tk.call('image', 'width', i[0].name))
                if tile_size == 16:
                    for j in range(len(i)):
                        i[j] = i[j].subsample(2)
                self.image_height = tile_size
                self.image_width = tile_size

    def get_row_location(self):
        return int(self.row_on_graphics // self.tile_size)

    def get_col_location(self):
        return self.col_on_graphics // self.tile_size

    def set_row_location(self, row: int):
        self.row_on_graphics = row * self.tile_size

    def set_col_location(self, col: int):
        self.col_on_graphics = col * self.tile_size

    def draw_the_image(self, parent):
        if self.image is not None:
            if type(self.image) is not list:
                if self.redraw:
                    self.redraw = False
                    parent.create_image(self.col_on_graphics, self.row_on_graphics, image=self.image, anchor=tk.NW)
            else:
                if self.redraw:
                    self.redraw = False
                    for i in self.image:
                        parent.create_image(self.col_on_graphics, self.row_on_graphics, image=i, anchor=tk.NW)

    def set_next_move(self, keyevent):
        keychar = keyevent.char
        if keychar == "":
            keychar = keyevent.keysym

        up = ["w", "W", "Up"]
        down = ["s", "S", "Down"]
        left = ["a", "A", "Left"]
        right = ["d", "D", "Right"]
        victory = ["v", "V"]
        pickup = [" "]

        if keychar in right:
            self.brain.add_next_move(AgentAction.moveRight)
        elif keychar in left:
            self.brain.add_next_move(AgentAction.moveLeft)
        elif keychar in up:
            self.brain.add_next_move(AgentAction.moveUp)
        elif keychar in down:
            self.brain.add_next_move(AgentAction.moveDown)
        elif keychar in victory:
            self.brain.add_next_move(AgentAction.declareVictory)
        elif keychar in pickup:
            self.brain.add_next_move(AgentAction.pickupSomething)
        else:
            print("Unknown key event " + str(keyevent))

    def get_move(self) -> AgentAction:
        return self.brain.get_next_move()

    def search(self, the_map: list[list[str]]):
        self.brain.search(the_map)
