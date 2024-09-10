from collections import deque
from lib.agent_action import AgentAction
from lib.game_state import GameState


class AgentBrain:

    def __init__(self):
        self.next_moves = deque()

    def add_next_move(self, next_move: AgentAction):
        self.next_moves.append(next_move)

    def clear_all_moves(self):
        self.next_moves = deque()

    def get_next_move(self) -> AgentAction:
        if len(self.next_moves) == 0:
            return AgentAction.doNothing
        return self.next_moves.pop()

    def search(self, game_map: list[list[str]]):
        # TODO: Change this to False
        use_only_key_listener = True
        if use_only_key_listener:
            # For Key Listener, and empty list
            self.next_moves = []
        else:
            # For code
            self.next_moves = GameState.search(game_map)

        # Just in case a student's code returns null
        if self.next_moves is None:
            self.next_moves = []
            self.next_moves.append(AgentAction.declareVictory)

        # Add up everything except doNothing and victory
        num = 0
        for i in range(len(self.next_moves)):
            if self.next_moves[i] != AgentAction.doNothing and self.next_moves[i] != AgentAction.declareVictory:
                num += 1
        print("Solution Depth =", num)
