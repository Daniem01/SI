from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random


class GoToCommandCenter(State):

    def __init__(self, id):
        super().__init__(id)
        self.Reset()

    def Start(self, agent):
        print("Inicio de estado GoToCommandCenter")

    def End(self):
        print("Fin de estado GoToCommandCenter")

    def Update(self, perception, map, agent):
        self.updateTime += perception[AgentConsts.TIME]
        if self.updateTime > 1.0:
            self.Reset()
        return self.action,True
    
    def Transit(self,perception, map):
        visible = perception[0:4]

        if (
            AgentConsts.PLAYER in visible or AgentConsts.OTHER in visible
        ) or (
            abs(perception[AgentConsts.AGENT_X] - perception[AgentConsts.PLAYER_X]) < 4
            and abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y])
            < 4
        ):
            return AgentConsts.STATE_ATTACK

        else:
            return None
    
    def Reset(self):
        self.action = random.randint(1,4)
        self.updateTime = 0