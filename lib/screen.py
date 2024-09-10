import tkinter as tk
import random
from pathlib import Path
from lib.game_object import GameObject
from lib.agent_action import AgentAction
from lib.variables import Variables

from lib.game_state_reversed import GameStateReversed


def find_random_image(folder_name: Path, bottom_starting_image=None):
    folder = folder_name
    files = list(folder.iterdir())
    num = random.randint(0, len(files) - 1)  # both inclusive
    f = files[num]
    while f.is_dir():  # 2 folders in that array
        f = files[random.randint(0, len(files) - 1)]

    # print(f.absolute())
    image = tk.PhotoImage(file=f.absolute())
    if bottom_starting_image:
        if type(bottom_starting_image) is not list:
            return [bottom_starting_image, image]
        else:
            bottom_starting_image.append(image)
            return bottom_starting_image
    return image


def sameSquare(a: GameObject, b: GameObject):
    if a.get_col_location() == b.get_col_location() and a.get_row_location() == b.get_row_location():
        return True
    return False


def exit_game():
    exit(0)


class Screen(tk.Canvas):

    def __init__(self, filename: Path):
        super(Screen, self).__init__()

        self.player = None
        self.ground = None
        self.wall = None
        self.screen = None
        self.map = None
        self.numEnemyHits = None
        self.playerDeclaresVictory = None
        self.numActions = None
        self.elixirs = None
        self.height = None
        self.width = None
        self.gold = None
        self.enemies = None
        self.startingGold = None
        self.coin = None
        self.the_map = []
        input_file = open(filename)
        contents = []

        for line in input_file:
            contents.append(line)

        self.rows = len(contents)
        self.cols = len(contents[0]) - 1  # newline at the end of each row

        for i in range(0, self.rows):
            self.the_map.append([])
            for j in range(0, self.cols):
                self.the_map[i].append(contents[i][j])

        input_file.close()

        print(self.the_map)

        # maps = GameStateReversed.createInitialGameStates(self.theMap)
        # for i in range(0,len(maps)):
        # 	print(maps[i])

        self.mapName = filename.name
        self.mapName = self.mapName[0:self.mapName.find(".")]
        self.setup_initial_variables()

        self.pack(fill="both", expand=True)
        self.draw_full_background()
        self.paint()

    def setup_initial_variables(self):
        # just in case things don't work so well with the map
        self.width = 10 * Variables.tileSize
        self.height = 10 * Variables.tileSize

        self.enemies = []
        self.gold = []
        self.elixirs = []

        self.numActions = 0
        self.playerDeclaresVictory = False
        self.numEnemyHits = 0

        self.map = [[None] * self.cols for _ in range(self.rows)]
        self.screen = [[None] * self.cols for _ in range(self.rows)]

        # Select the images to use for this run
        self.wall = find_random_image(Path("images", "Dungeon Crawl Stone Soup Full", "dungeon", "wall"))
        self.ground = find_random_image(Path("images", "Dungeon Crawl Stone Soup Full", "dungeon", "floor"))
        if Variables.tileSize == 16:
            self.wall = self.wall.subsample(2, 2)
            self.ground = self.ground.subsample(2, 2)

        # print("again", self.rows, self.cols)
        # print(self.screen)

        for i in range(0, self.rows):
            # print("row",i)
            for j in range(0, self.cols):
                # print("col",j)
                if self.the_map[i][j] == Variables.S_WALL:
                    self.screen[i][j] = self.wall
                elif self.the_map[i][j] == Variables.S_GROUND:
                    self.screen[i][j] = self.ground
                elif self.the_map[i][j] == Variables.S_PLAYER:
                    self.screen[i][j] = self.ground
                    self.load_player_image(j, i)
                elif self.the_map[i][j] == Variables.S_PLAYER_AND_GOLD:
                    self.screen[i][j] = self.ground
                    self.coin = find_random_image(Path("images", "Dungeon Crawl Stone Soup Full", "item", "gold"))
                    self.gold.append(
                        GameObject(j * Variables.tileSize, i * Variables.tileSize, coin, Variables.tileSize))
                    self.load_player_image(j, i)
                elif self.the_map[i][j] == Variables.S_GOLD:
                    # put the gold on the ground
                    coin = find_random_image(Path("images", "Dungeon Crawl Stone Soup Full", "item", "gold"))
                    self.gold.append(
                        GameObject(j * Variables.tileSize, i * Variables.tileSize, coin, Variables.tileSize))
                    self.screen[i][j] = self.ground
                elif self.the_map[i][j] == Variables.S_ENEMY:
                    enemy = find_random_image(Path("images", "Dungeon Crawl Stone Soup Full", "monster"))
                    self.enemies.append(
                        GameObject(j * Variables.tileSize, i * Variables.tileSize, enemy, Variables.tileSize))
                    self.screen[i][j] = self.ground
                elif self.the_map[i][j] == Variables.S_ELIXER:
                    elixir = find_random_image(Path("images", "Dungeon Crawl Stone Soup Full", "item", "potion"))
                    self.elixirs.append(
                        GameObject(j * Variables.tileSize, i * Variables.tileSize, elixir, Variables.tileSize))
                    self.screen[i][j] = self.ground
                else:
                    print("Unhandled case: '" + self.the_map[i][j] + "'")
                    raise AttributeError()
                self.map[i][j] = self.the_map[i][j]

        self.startingGold = len(self.gold)

        self.player.search(self.map)

        # self.setSize(self.cols*Variables.tileSize,self.rows*Variables.tileSize)
        self.width = self.cols * Variables.tileSize
        self.height = self.rows * Variables.tileSize

    def load_player_image(self, col: int, row: int):
        player_image = find_random_image(Path("images", "Dungeon Crawl Stone Soup Full", "player", "base"))
        player_image = find_random_image(Path("images", "Dungeon Crawl Stone Soup Full", "player", "cloak"),
                                         bottom_starting_image=player_image)
        player_image = find_random_image(Path("images", "Dungeon Crawl Stone Soup Full", "player", "boots"),
                                         bottom_starting_image=player_image)
        player_image = find_random_image(Path("images", "Dungeon Crawl Stone Soup Full", "player", "gloves"),
                                         bottom_starting_image=player_image)
        player_image = find_random_image(
            Path("images", "Dungeon Crawl Stone Soup Full", "player", "draconic_head"),
            bottom_starting_image=player_image)
        player_image = find_random_image(
            Path("images", "Dungeon Crawl Stone Soup Full", "player", "draconic_wing"),
            bottom_starting_image=player_image)
        self.player = GameObject(col * Variables.tileSize, row * Variables.tileSize, player_image, Variables.tileSize)

    def isValidMove(self, new_row: int, new_col: int):
        if 0 <= new_row < len(self.screen) and 0 <= new_col < len(self.screen[0]):
            if self.screen[new_row][new_col] == self.ground:
                return True
            else:
                if self.screen[new_row][new_col] == self.wall:
                    pass
        else:
            print("Out of bounds")

        return False

    def move(self, g: GameObject):
        action = g.get_move()
        if action is None:
            return

        col = g.get_col_location()
        row = g.get_row_location()

        if action == AgentAction.declareVictory:
            self.playerDeclaresVictory = True

        elif action == AgentAction.pickupSomething:
            self.player.redraw = True
            for go in self.gold:
                if go.get_col_location() == col and go.get_row_location() == row:
                    self.gold.remove(go)
                    # re-draw that square
                    self.create_image(col * Variables.tileSize, row * Variables.tileSize, image=self.screen[row][col],
                                      anchor=tk.NW)
                    break  # assume only 1 gold can be picked up at a time

            for go in self.elixirs:
                if go.get_col_location() == col and go.get_row_location() == row:
                    self.elixirs.remove(go)
                    # re-draw that square
                    self.create_image(col * Variables.tileSize, row * Variables.tileSize, image=self.screen[row][col],
                                      anchor=tk.NW)
                    break  # assume only 1 elixir can be picked up at a time

        elif action == AgentAction.moveRight:
            if self.isValidMove(row, col + 1):
                self.update_objects_that_need_to_redraw(row, col)
                g.set_col_location(col + 1)
        elif action == AgentAction.moveLeft:
            if self.isValidMove(row, col - 1):
                self.update_objects_that_need_to_redraw(row, col)
                g.set_col_location(col - 1)
        elif action == AgentAction.moveUp:
            if self.isValidMove(row - 1, col):
                self.update_objects_that_need_to_redraw(row, col)
                g.set_row_location(row - 1)
        elif action == AgentAction.moveDown:
            if self.isValidMove(row + 1, col):
                self.update_objects_that_need_to_redraw(row, col)
                g.set_row_location(row + 1)
        elif action == AgentAction.doNothing:
            pass
        else:
            print("Unhandled action " + str(action))

        if action.is_an_action:
            self.numActions += 1

    def update_objects_that_need_to_redraw(self, row: int, col: int):
        self.player.redraw = True
        self.create_image(col * Variables.tileSize, row * Variables.tileSize, image=self.screen[row][col], anchor=tk.NW)
        # for i in range(0,self.rows):
        # 	for j in range(0,self.cols):
        # 		self.create_image(j*Variables.tileSize, i*Variables.tileSize,image=self.screen[i][j], anchor=tk.NW)
        for g in self.gold:
            if g.get_col_location() == col and g.get_row_location() == row:
                g.redraw = True
        for g in self.elixirs:
            if g.get_col_location() == col and g.get_row_location() == row:
                g.redraw = True
        for g in self.enemies:
            if g.get_col_location() == col and g.get_row_location() == row:
                g.redraw = True

    def paint(self):

        if self.playerDeclaresVictory:
            print("Map: " + self.mapName)
            print("Gold Remaining " + str(len(self.gold)) + " of " + str(self.startingGold))
            print("Total Actions: " + str(self.numActions))
            print("Enemy Hits: " + str(self.numEnemyHits))
            self.after(Variables.SLEEP_TIME * 3, exit_game)
            return
        else:
            self.move(self.player)

        # draw the gold
        for g in self.gold:
            g.draw_the_image(self)

        # draw the elixirs
        for g in self.elixirs:
            g.draw_the_image(self)

        # draw the enemies
        for g in self.enemies:
            g.draw_the_image(self)
            if sameSquare(self.player, g):
                self.numEnemyHits += 1
                print("Hit an enemy")

        self.player.draw_the_image(self)

        self.after(Variables.SLEEP_TIME, self.paint)

    def draw_full_background(self):
        if self.screen is not None:
            for i in range(0, self.rows):
                for j in range(0, self.cols):
                    self.create_image(j * Variables.tileSize, i * Variables.tileSize, image=self.screen[i][j],
                                      anchor=tk.NW)
