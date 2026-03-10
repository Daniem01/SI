from StateMachine.State import State
from States.AgentConsts import AgentConsts


class AttackPlayer(State):

    # Funcion init
    def __init__(self, id):
        super().__init__(id)
        self.obstaculos = [
            AgentConsts.UNBREAKABLE,
            AgentConsts.SEMI_UNBREKABLE,
            AgentConsts.OTHER,
        ]

    def Start(self, agent):
        print("Empieza estado AttackPlayer")

    def End(self):
        print("Fin del estado AttackPlayer")

    # Funcion auxiliar para procesar los movimientos en update
    def ProcesaMovimiento(self, intencionMov, perception):
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

        # Si hay un obstaculo avanzamos sin disparar
        if (
            perception[sensor_frente] in self.obstaculos
            and perception[distancia_frente] > 1
        ):
            return intencionMov, False
        # Si el obstaculo nos cierra el paso miramos opciones
        elif (
            perception[sensor_frente] in self.obstaculos
            and perception[distancia_frente] <= 1
        ):
            if (
                perception[sensor_lado1] in self.obstaculos
                and perception[distancia_lado1] <= 1
            ):
                if (
                    perception[sensor_lado2] in self.obstaculos
                    and perception[distancia_lado2] <= 1
                ):
                    return accion_atras, False
                else:
                    return accion_lado2, False
            else:
                return accion_lado1, False
        else:
            return intencionMov, True

    # Update
    def Update(self, perception, map, agent):
        if isinstance(perception, bool) or perception is None:
            return "none", False
        # Primero debemos mirar en que direccion debe ir el tanque
        # en funcion de donde esta el enemigo para "apuntar"

        # Si el agente y el jugador estan en la misma columna
        if perception[AgentConsts.AGENT_X] == perception[AgentConsts.PLAYER_X]:
            if perception[AgentConsts.AGENT_Y] < perception[AgentConsts.PLAYER_Y]:
                intencion = AgentConsts.MOVE_DOWN
                return self.ProcesaMovimiento(intencion, perception)
            else:
                intencion = AgentConsts.MOVE_UP
                return self.ProcesaMovimiento(intencion, perception)

        # Si el agente y el jugador estan en la misma fila
        elif perception[AgentConsts.AGENT_Y] == perception[AgentConsts.PLAYER_Y]:
            if perception[AgentConsts.AGENT_X] < perception[AgentConsts.PLAYER_X]:
                intencion = AgentConsts.MOVE_RIGHT
                return self.ProcesaMovimiento(intencion, perception)
            else:
                intencion = AgentConsts.MOVE_LEFT
                return self.ProcesaMovimiento(intencion, perception)

        # Si no estan alineados pero esta cerca querremos que intente alinearse con el jugador
        # para poder intentar destruirlo
        else:
            # Si el jugador es mas facil alinearlo en el eje x
            if abs(
                perception[AgentConsts.AGENT_X] - perception[AgentConsts.PLAYER_X]
            ) > abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y]):
                if perception[AgentConsts.AGENT_Y] < perception[AgentConsts.PLAYER_Y]:
                    intencion = AgentConsts.MOVE_DOWN
                    return self.ProcesaMovimiento(intencion, perception)
                else:
                    intencion = AgentConsts.MOVE_UP
                    return self.ProcesaMovimiento(intencion, perception)
            # Si es mas facil alinarlo con el eje y
            else:
                if perception[AgentConsts.AGENT_X] < perception[AgentConsts.PLAYER_X]:
                    intencion = AgentConsts.MOVE_RIGHT
                    return self.ProcesaMovimiento(intencion, perception) 
                else:
                    intencion = AgentConsts.MOVE_LEFT
                    return self.ProcesaMovimiento(intencion, perception)

    def Transit(self, perception, map):
        if isinstance(perception, bool) or perception is None:
            return "none", False
        
        # Pasar a GoToCommandCerter
        visible = perception[0:4]

        if (
            AgentConsts.PLAYER not in visible and AgentConsts.OTHER not in visible
        ) and (
            abs(perception[AgentConsts.AGENT_X] - perception[AgentConsts.PLAYER_X]) >= 4
            or abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y])
            >= 4
        ):
            return AgentConsts.STATE_GO_CENTER

        else:
            return AgentConsts.STATE_ATTACK
