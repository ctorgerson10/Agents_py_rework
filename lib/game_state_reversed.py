from lib.game_state import GameState
from lib.variables import Variables


class GameStateReversed(GameState):

    #This constructor assumes that it is being created as a child from the existing s
    def __init__(self, parent_state=None, newX=-1, newY=-1, map=None):
        if map == None:
            super().__init__(None, parent_state=parent_state, newX=newX, newY=newY)
        else:
            #Probably don't call this one, except from the createInitialGameStates method
            super().__init__(map)

    def getNextStates(self):
        #TODO
        return None

    @staticmethod
    def createInitialGameStates(map):
        #Figure out how many gold
        startingMap = []
        numInitialStates = 0
        for i in range(0, len(map)):
            startingMap.append([])
            for j in range(0, len(map[i])):
                startingMap[i].append(map[i][j])
                if map[i][j] == Variables.S_GOLD:
                    numInitialStates += 1
                    startingMap[i][j] = Variables.S_MISSING_GOLD
                elif map[i][j] == Variables.S_PLAYER_AND_GOLD:
                    numInitialStates += 1
                    startingMap[i][j] = Variables.S_MISSING_GOLD  #We will put the player on every gold
                elif (map[i][j] == Variables.S_PLAYER):
                    startingMap[i][
                        j] = Variables.S_GROUND  #We will put the player on every gold, so remove it from where it is
        #create blank states
        gss = []
        for i in range(0, numInitialStates):
            gss.append([])
        currentNum = 0
        #Put player on every missing gold, as they all could potentially be the "last" gold we pickup
        for i in range(0, len(startingMap)):
            for j in range(0, len(startingMap[i])):
                if startingMap[i][j] == Variables.S_MISSING_GOLD:
                    startingMap[i][j] = Variables.S_PLAYER_AND_MISSING_GOLD
                    gss[currentNum] = GameStateReversed(map=startingMap)
                    currentNum += 1
                    startingMap[i][j] = Variables.S_MISSING_GOLD
        return gss
