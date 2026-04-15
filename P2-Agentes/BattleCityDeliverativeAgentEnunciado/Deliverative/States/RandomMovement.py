from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class RandomMovement(State):

    def __init__(self, id):
        super().__init__(id)

    def Start(self, agent):
        super().Start(agent)
        self.action = random.randint(1, 4)
        self.startTime = None

    def Update(self, perception, map, agent):
        return self.action, True

    def Transit(self, perception, map):
        if self.startTime is None:
            self.startTime = perception[AgentConsts.TIME]

        if perception[AgentConsts.TIME] - self.startTime > 0.4:
            return "ExecutePlan"
        return self.id