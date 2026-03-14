from StateMachine.State import State
from States.AgentConsts import AgentConsts

class AttackPlayer(State):

    def __init__(self, id):
        super().__init__(id)
        self.indestructibles = [
            AgentConsts.UNBREAKABLE,
            AgentConsts.SEMI_UNBREKABLE,
            AgentConsts.OTHER,
        ]

    def Start(self, agent):
        print("Empieza estado AttackPlayer")

    def End(self):
        print("Fin del estado AttackPlayer")

    def ProcesaMovimiento(self, intencionMov, perception, alineado):
        # Down
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
        #Up
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
        # Right
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
        #Left
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

        disparar = alineado or (perception[sensor_frente] == AgentConsts.BRICK)

        if (perception[sensor_frente] in self.indestructibles and perception[distancia_frente] > 1):
            return intencionMov, disparar
        elif (perception[sensor_frente] in self.indestructibles and perception[distancia_frente] <= 1):
            if (perception[sensor_lado1] in self.indestructibles and perception[distancia_lado1] <= 1):
                if (perception[sensor_lado2] in self.indestructibles and perception[distancia_lado2] <= 1):
                    return accion_atras, disparar
                else:
                    return accion_lado2, disparar
            else:
                return accion_lado1, disparar
        else:
            return intencionMov, disparar

    def Update(self, perception, map, agent):
        if isinstance(perception, bool) or perception is None:
            return "none", False

        # Como hay decimales es dificil que sea exactas ciertas comparaciones con las posiciones asi que usamos aproximaciones
        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        px, py = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        
        alineado_x = abs(ax - px) < 0.5
        alineado_y = abs(ay - py) < 0.5

<<<<<<< Updated upstream
        if alineado_x:
            intencion = AgentConsts.MOVE_DOWN if ay < py else AgentConsts.MOVE_UP
=======
        # SIEMPRE calcular esto primero
        alineado_x = abs(ax - px) < 0.8
        alineado_y = abs(ay - py) < 0.8

        # stuck detection
        if self.prev_pos == (ax, ay) and self.last_action is not None:
            self.stuck_count += 1
        else:
            self.stuck_count = 0
        self.prev_pos = (ax, ay)

        # distancia al jugador
        dist = abs(ax - px) + abs(ay - py)
        if self.avoid_steps > 0 and self.prev_distance is not None and dist < self.prev_distance:
            self.avoid_steps = 0
            self.avoid_direction = None

        # if currently avoiding, stick to avoid_direction for limited steps
        if self.avoid_steps > 0 and self.avoid_direction is not None:
            print("ATT continuing avoidance", self.avoid_direction, "steps", self.avoid_steps)
            intencion = self.avoid_direction
            self.avoid_steps -= 1
        else:
            alineado_x = abs(ax - px) < 0.8
            alineado_y = abs(ay - py) < 0.8

            if alineado_x:
                intencion = AgentConsts.MOVE_DOWN if ay < py else AgentConsts.MOVE_UP
            elif alineado_y:
                intencion = AgentConsts.MOVE_RIGHT if ax < px else AgentConsts.MOVE_LEFT
            else:
                # Intentamos alinearnos con el tanque enemigo para tener linea de fuego
                dx = abs(ax - px)
                dy = abs(ay - py)
                if dx > dy:
                    intencion = AgentConsts.MOVE_RIGHT if ax < px else AgentConsts.MOVE_LEFT
                elif dx < dy:
                    intencion = AgentConsts.MOVE_DOWN if ay < py else AgentConsts.MOVE_UP
                else:
                    if self.last_intention is not None:
                        intencion = self.last_intention
                    else:
                        intencion = AgentConsts.MOVE_RIGHT if ax < px else AgentConsts.MOVE_LEFT

        # If stuck a few ticks, force right turn
        if self.stuck_count > 2:
            intencion = AgentConsts.MOVE_RIGHT
            self.stuck_count = 0

        # Guarda la intención anterior para evitar bailes 
        self.last_intention = intencion
        self.prev_distance = dist
        if alineado_x or alineado_y:
>>>>>>> Stashed changes
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
        if isinstance(perception, bool) or perception is None: return AgentConsts.STATE_ATTACK

        px, py = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]

        # Si el jugador muere se vuelve a GTCC
        if px < 0:
            return AgentConsts.STATE_GO_CENTER 

        # Si se aleja mucho el jugador volvemos a GTCC
        distancia = abs(ax - px) + abs(ay - py)
        if distancia > 5.0:
            return AgentConsts.STATE_GO_CENTER

        return AgentConsts.STATE_ATTACK