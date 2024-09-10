from collections import deque
from lib.agent_action import AgentAction
from lib.game_state import GameState


class AgentBrain:

    def __init__(self):
        self.nextMoves = deque()

    def addNextMove(self, nextMove: AgentAction):
        self.nextMoves.append(nextMove)

    def clearAllMoves(self):
        self.nextMoves = deque()

    def getNextMove(self) -> AgentAction:
        if len(self.nextMoves) == 0:
            return AgentAction.doNothing
        return self.nextMoves.pop(0)

    def search(self, map: list[list[str]]):

        # TODO: Change this to False
        useOnlyKeyListener = True
        if useOnlyKeyListener:
            #For Key Listener, and empty list
            self.nextMoves = []
        else:
            #For code
            self.nextMoves = GameState.search(map)

        # Just in case a student's code returns null
        if self.nextMoves == None:
            self.nextMoves = []
            self.nextMoves.add(AgentAction.declareVictory)

        # Add up everything except doNothing and victory
        num = 0
        for i in range(0, len(self.nextMoves)):
            if (self.nextMoves[i] != AgentAction.doNothing and self.nextMoves[i] != AgentAction.declareVictory):
                num += 1
        print("Solution Depth =", num)
