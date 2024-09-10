from lib.game_state import GameState
from lib.variables import Variables


class GameStateReversed(GameState):

    # This constructor assumes that it is being created as a child from the existing s
    def __init__(self, parent_state=None, new_x=-1, new_y=-1, game_map=None):
        if game_map is None:
            super().__init__(None, parent_state=parent_state, new_x=new_x, new_y=new_y)
        else:
            # Probably don't call this one, except from the createInitialGameStates method
            super().__init__(game_map)

    def get_next_states(self):
        # TODO
        return None

    @staticmethod
    def create_initial_game_states(map):
        # Figure out how many gold
        starting_map = []
        num_initial_states = 0
        for i in range(len(map)):
            starting_map.append([])
            for j in range(len(map[i])):
                starting_map[i].append(map[i][j])
                if map[i][j] == Variables.S_GOLD:
                    num_initial_states += 1
                    starting_map[i][j] = Variables.S_MISSING_GOLD
                elif map[i][j] == Variables.S_PLAYER_AND_GOLD:
                    num_initial_states += 1
                    starting_map[i][j] = Variables.S_MISSING_GOLD  # We will put the player on every gold
                elif map[i][j] == Variables.S_PLAYER:
                    starting_map[i][
                        j] = Variables.S_GROUND  # We will put the player on every gold, so remove it from where it is
        # create blank states
        gss = []
        for i in range(num_initial_states):
            gss.append([])
        current_num = 0
        # Put player on every missing gold, as they all could potentially be the "last" gold we pickup
        for i in range(len(starting_map)):
            for j in range(len(starting_map[i])):
                if starting_map[i][j] == Variables.S_MISSING_GOLD:
                    starting_map[i][j] = Variables.S_PLAYER_AND_MISSING_GOLD
                    gss[current_num] = GameStateReversed(game_map=starting_map)
                    current_num += 1
                    starting_map[i][j] = Variables.S_MISSING_GOLD
        return gss
