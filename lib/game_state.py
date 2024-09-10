from lib.agent_action import AgentAction
from lib.variables import Variables


class GameState:

    # This constructor assumes that there is an 'S' somewhere on the map and the game is just starting
    # i.e., no parent node, and no distance
    def __init__(self, game_map, parent_state=None, new_x=-1, new_y=-1):
        GameState.num_nodes_created += 1  # One more node created
        self.map = None

        # x and y are the locations of the character on the map
        self.row = 0
        self.col = 0
        # Action will be the action we take. Note: Do not create "new" ones, just use the existing static ones
        self.action = None

        # For now, we will say that two states are the same if they have the same string representation
        # Currently build like "x y mapCharactersHere"
        self.stringRepresentationOfState = None  # We may need to do lazy instantiation on this, if it is slow

        # Parent is the GameState that generated this one
        if parent_state is None:
            self.parent = None
            # Distance is the current distance the character traveled to get to this location, not how far remaining
            self.current_distance = 0
            new_x = -1
            new_y = -1
            self.map = []
            for i in range(len(game_map)):
                self.map.append([])
                for j in range(len(game_map[0])):
                    # Copy things over
                    self.map[i].append(game_map[i][j])

                    # Remove the player from the map
                    if self.map[i][j] == Variables.S_PLAYER_AND_MISSING_GOLD:
                        new_x = i
                        new_y = j
                        self.map[i][j] = Variables.S_MISSING_GOLD  # Remove the player
                    elif self.map[i][j] == Variables.S_PLAYER_AND_GOLD:
                        new_x = i
                        new_y = j
                        self.map[i][j] = Variables.S_GOLD  # Remove the player from the map
                    elif self.map[i][j] == Variables.S_PLAYER:
                        new_x = i
                        new_y = j
                        self.map[i][j] = Variables.S_GROUND  # Remove the player from the map
                    else:
                        # things are fine
                        pass

                self.row = new_x
                self.col = new_y
        else:
            self.parent = parent_state
            self.current_distance = parent_state.current_distance + 1
            self.row = new_x
            self.col = new_y
            self.map = []
            for i in range(len(game_map)):
                self.map.append([])
                for j in range(len(game_map[0])):
                    self.map[i].append(game_map[i][j])

        self.rebuild_string_representation()

    def __str__(self):
        return self.stringRepresentationOfState

    def __hash__(self) -> int:
        return self.stringRepresentationOfState.__hash__()

    # TODO - you can leave this for now, but when we are implementing a priority queue, we will likely have to change it
    # To compare estimated distance from goal
    def __lt__(self, other):
        return self.stringRepresentationOfState < other.stringRepresentationOfState

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        return (self.stringRepresentationOfState == other.stringRepresentationOfState and
                self.stringRepresentationOfState == other.stringRepresentationOfState)

    def __ne__(self, other):
        return not self.__eq__(other)

    def change_gold_to_ground(self, row, col):
        if 0 <= row <= len(self.map) and 0 <= col < len(self.map[0]) and self.map[row][col] == Variables.S_GOLD:
            self.map[row][col] = Variables.S_GROUND
            self.rebuild_string_representation()

    def change_missing_gold_to_gold(self, row, col):
        if 0 <= row <= len(self.map) and 0 <= col < len(self.map[0]) and self.map[row][col] == Variables.S_MISSING_GOLD:
            self.map[row][col] = Variables.S_GOLD
            self.rebuild_string_representation()

    def rebuild_string_representation(self):
        sb = ""
        for i in range(0, len(self.map)):
            for j in range(0, len(self.map[i])):
                # Patch if necessary
                if self.map[i][j] == Variables.S_MISSING_GOLD:
                    sb = sb + Variables.S_GROUND  # Keep the missing gold, but put ground in our state
                else:
                    sb = sb + self.map[i][j]
        self.stringRepresentationOfState = str(self.row) + " " + str(self.col) + " " + sb

    def print_maze(self):
        for i in len(self.map):
            for j in len(self.map[i]):
                if i == self.row and j == self.col:
                    if self.map[i][j] == Variables.S_GOLD:
                        print(Variables.S_PLAYER_AND_GOLD, end="")
                    else:
                        print(Variables.S_PLAYER, end="")
                else:
                    print(self.map[i][j], end="")
            print("")

    def get_all_actions(self):
        if self.parent is None:
            moves = []
            if self.action is not None:
                moves.append(self.action)
            return moves
        else:
            moves = self.parent.get_all_actions()
            moves.append(self.action)
            return moves

    def is_goal_state(self):
        # TODO
        return True

    def get_next_states(self):
        # TODO
        return None

    @staticmethod
    def search(problem):
        # TODO, change this next line as we introduce different types of search
        return GameState.breadth_first_search(problem)

    @staticmethod
    def breadth_first_search(problem):
        # Some static variables so that we can determine how "hard" problems are
        GameState.num_nodes_explored = 0
        GameState.num_nodes_created = 0

        node = GameState(problem)  # Essentially the second line of the book's BFS
        if node.is_goal_state():  # Essentially the start of line 3 of the book's BFS
            node.action = AgentAction.declareVictory  # We don't have to do anything
            return node.get_all_actions()  # Just the single thing, but this is an example for later

        # Create the frontier queue, and reached hash
        frontier = []
        reached = set()

        # Add the first node to the hash
        reached.add(node)

        # TODO - create the rest of the BFS function

        # node = frontier.pop(0) #retrieve and remove

        GameState.num_nodes_explored += 1  # we are now ready to "explore" the starting node

        # Print this at the end, so we know how "hard" the problem was
        print("Number of nodes explored =", GameState.num_nodes_explored)
        print("Number of nodes created =", GameState.num_nodes_created)

        # return the goalNode.getAllActions() if you find a goal node

        return None


GameState.num_nodes_explored = 0
GameState.num_nodes_created = 0
