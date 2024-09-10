class AgentAction:

    def __init__(self, isAnAction: bool):
        self.isAnAction = isAnAction

    def __str__(self):
        if self == AgentAction.moveLeft:
            return "Move Left"
        elif self == AgentAction.moveRight:
            return "Move Right"
        elif self == AgentAction.moveUp:
            return "Move Up"
        elif self == AgentAction.moveDown:
            return "Move Down"
        elif self == AgentAction.pickupSomething:
            return "Pickup Something"
        elif self == AgentAction.declareVictory:
            return "Declare Victory"
        elif self == AgentAction.doNothing:
            return "Do Nothing"
        return "Unknown Action"


AgentAction.moveLeft = AgentAction(True)
AgentAction.moveRight = AgentAction(True)
AgentAction.moveUp = AgentAction(True)
AgentAction.moveDown = AgentAction(True)

AgentAction.pickupSomething = AgentAction(True)
AgentAction.declareVictory = AgentAction(False)

AgentAction.doNothing = AgentAction(False)
