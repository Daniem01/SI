from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Attack(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):
        direction = agent.directionToLook
        target = perception[direction]

        # si tenemos el objetivo delante y podemos disparar, disparamo
        if target in (AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER) and perception[AgentConsts.CAN_FIRE] == 1:
            return AgentConsts.NO_MOVE, True

        # si no puedo disparar aun, sigo orientandome en esa direccion
        move = direction + 1  # perception dir 0..3 -> move 1..4
        return move, False

    def Transit(self, perception, map):
        target = perception[self.directionToLook] if hasattr(self, "directionToLook") else -1
        if target not in (AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER):
            return "ExecutePlan"
        return self.id