from StateMachine.State import State
from States.AgentConsts import AgentConsts

class AttackPlayer(State):

    def __init__(self, id):
        super().__init__(id)
        self.obstaculos = [
            AgentConsts.UNBREAKABLE,
            AgentConsts.SEMI_UNBREKABLE,
            AgentConsts.OTHER,
        ]

    def Start(self, agent):
        print("Empieza estado AttackPlayer")

    def End(self, agent):
        print("Fin del estado AttackPlayer")

    # CAMBIO 2: Añadido parámetro 'puede_disparar' para controlar el fuego
    def ProcesaMovimiento(self, intencionMov, perception, puede_disparar):
        if intencionMov == AgentConsts.MOVE_DOWN:
            sensor_frente = AgentConsts.NEIGHBORHOOD_DOWN
            distancia_frente = AgentConsts.NEIGHBORHOOD_DIST_DOWN
            sensor_lado1 = AgentConsts.NEIGHBORHOOD_RIGHT
            distancia_lado1 = AgentConsts.NEIGHBORHOOD_DIST_RIGHT
            sensor_lado2 = AgentConsts.NEIGHBORHOOD_LEFT
            distancia_lado2 = AgentConsts.NEIGHBORHOOD_DIST_LEFT
            accion_lado1 = AgentConsts.MOVE_RIGHT
            accion_lado2 = AgentConsts.MOVE_LEFT
            accion_atras = AgentConsts.MOVE_UP
        elif intencionMov == AgentConsts.MOVE_UP:
            sensor_frente = AgentConsts.NEIGHBORHOOD_UP
            distancia_frente = AgentConsts.NEIGHBORHOOD_DIST_UP
            sensor_lado1 = AgentConsts.NEIGHBORHOOD_LEFT
            distancia_lado1 = AgentConsts.NEIGHBORHOOD_DIST_LEFT
            sensor_lado2 = AgentConsts.NEIGHBORHOOD_RIGHT
            distancia_lado2 = AgentConsts.NEIGHBORHOOD_DIST_RIGHT
            accion_lado1 = AgentConsts.MOVE_LEFT
            accion_lado2 = AgentConsts.MOVE_RIGHT
            accion_atras = AgentConsts.MOVE_DOWN
        elif intencionMov == AgentConsts.MOVE_RIGHT:
            sensor_frente = AgentConsts.NEIGHBORHOOD_RIGHT
            distancia_frente = AgentConsts.NEIGHBORHOOD_DIST_RIGHT
            sensor_lado1 = AgentConsts.NEIGHBORHOOD_UP
            distancia_lado1 = AgentConsts.NEIGHBORHOOD_DIST_UP
            sensor_lado2 = AgentConsts.NEIGHBORHOOD_DOWN
            distancia_lado2 = AgentConsts.NEIGHBORHOOD_DIST_DOWN
            accion_lado1 = AgentConsts.MOVE_UP
            accion_lado2 = AgentConsts.MOVE_DOWN
            accion_atras = AgentConsts.MOVE_LEFT
        else:
            sensor_frente = AgentConsts.NEIGHBORHOOD_LEFT
            distancia_frente = AgentConsts.NEIGHBORHOOD_DIST_LEFT
            sensor_lado1 = AgentConsts.NEIGHBORHOOD_DOWN
            distancia_lado1 = AgentConsts.NEIGHBORHOOD_DIST_DOWN
            sensor_lado2 = AgentConsts.NEIGHBORHOOD_UP
            distancia_lado2 = AgentConsts.NEIGHBORHOOD_DIST_UP
            accion_lado1 = AgentConsts.MOVE_DOWN
            accion_lado2 = AgentConsts.MOVE_UP
            accion_atras = AgentConsts.MOVE_RIGHT

        if (perception[sensor_frente] in self.obstaculos and perception[distancia_frente] > 1):
            return intencionMov, False
        elif (perception[sensor_frente] in self.obstaculos and perception[distancia_frente] <= 1):
            if (perception[sensor_lado1] in self.obstaculos and perception[distancia_lado1] <= 1):
                if (perception[sensor_lado2] in self.obstaculos and perception[distancia_lado2] <= 1):
                    return accion_atras, False
                else:
                    return accion_lado2, False
            else:
                return accion_lado1, False
        else:
            return intencionMov, puede_disparar

    def Update(self, perception, map, agent):
        if isinstance(perception, bool) or perception is None:
            return "none", False

        # Como hay decimales es dificil que sea exactas ciertas comparaciones con las posiciones asi que usamos aproximaciones
        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        px, py = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        
        alineado_x = abs(ax - px) < 0.5
        alineado_y = abs(ay - py) < 0.5

        if alineado_x:
            intencion = AgentConsts.MOVE_DOWN if ay < py else AgentConsts.MOVE_UP
            return self.ProcesaMovimiento(intencion, perception, True)
        elif alineado_y:
            intencion = AgentConsts.MOVE_RIGHT if ax < px else AgentConsts.MOVE_LEFT
            return self.ProcesaMovimiento(intencion, perception, True) 
        else:
            # Si no está alineado busca alinearse para atacar
            if abs(ax - px) > abs(ay - py):
                intencion = AgentConsts.MOVE_DOWN if ay < py else AgentConsts.MOVE_UP
            else:
                intencion = AgentConsts.MOVE_RIGHT if ax < px else AgentConsts.MOVE_LEFT
            return self.ProcesaMovimiento(intencion, perception, False)

    def Transit(self, perception, map):
        if isinstance(perception, bool) or perception is None:
            return AgentConsts.STATE_ATTACK
        
        visible = perception[0:4]
        dist_x = abs(perception[AgentConsts.AGENT_X] - perception[AgentConsts.PLAYER_X])
        dist_y = abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y])

        # Si el jugador ya no es visible o se ha alejado mucho
        if (AgentConsts.PLAYER not in visible and AgentConsts.OTHER not in visible) and (dist_x >= 4 or dist_y >= 4):
            return AgentConsts.STATE_GO_CENTER
        else:
            return AgentConsts.STATE_ATTACK