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
        if isinstance(perception, bool) or perception is None:
            return "none", False
    
        self.updateTime += perception[AgentConsts.TIME]
        if self.updateTime > 1.0:
            self.Reset()
        return self.action,True
    
    def Transit(self, perception, map):
        if isinstance(perception, bool) or perception is None: return AgentConsts.STATE_GO_CENTER

        px, py = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        cx, cy = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]

        # Buscar la salida
        #if cx < 0 or px < 0:
        #    return AgentConsts.STATE_FIND_EXIT

        # Si detectamos al jugador cerca cambiamos a attackPlayer
        if px != -1:
            distancia = abs(ax - px) + abs(ay - py)
            if distancia < 7.0:
                return AgentConsts.STATE_ATTACK
            
        return AgentConsts.STATE_GO_CENTER
    
    def Reset(self):
        self.action = random.randint(1,4)
        self.updateTime = 0