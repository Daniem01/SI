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
        self.last_action = None
        self.last_intention = None
        self.prev_pos = None
        self.stuck_count = 0
        self.avoid_direction = None
        self.avoid_steps = 0
        self.prev_distance = None

    def Start(self, agent):
        print("Empieza estado AttackPlayer")

    def End(self):
        print("Fin del estado AttackPlayer")

    def ProcesaMovimiento(self, intencionMov, perception, alineado):
        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        px, py = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        print(f"ATT ProcesaMovimiento pos=({ax:.1f},{ay:.1f}) inten={intencionMov} last={self.last_action} stuck={self.stuck_count}")
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

        if perception[sensor_frente] in self.indestructibles:
            print("ATT detected indestructible in front", perception[sensor_frente])
            opciones = []
            if (perception[sensor_lado1] not in self.indestructibles and perception[distancia_lado1] > 1):
                opciones.append(accion_lado1)
            if (perception[sensor_lado2] not in self.indestructibles and perception[distancia_lado2] > 1):
                opciones.append(accion_lado2)

            if opciones:
                if self.last_action in opciones and len(opciones) > 1:
                    resultado = opciones[1]
                else:
                    resultado = opciones[0]
                self.last_action = resultado
                self.avoid_direction = resultado
                self.avoid_steps = 2
                return resultado, disparar
            else:
                # Esquina cerrada -> giramos derecha
                if self.stuck_count > 0:
                    for alt in (AgentConsts.MOVE_DOWN, AgentConsts.MOVE_LEFT, AgentConsts.MOVE_UP):
                        if alt != intencionMov:
                            self.last_action = alt
                            self.avoid_direction = alt
                            self.avoid_steps = 2
                            return alt, disparar
                self.last_action = accion_lado1
                self.avoid_direction = accion_lado1
                self.avoid_steps = 2
                return accion_lado1, disparar
        
        if self.avoid_direction is not None and perception[sensor_frente] not in self.indestructibles:
            self.avoid_direction = None

        self.last_action = intencionMov
        return intencionMov, disparar

    def Update(self, perception, map, agent):
        if isinstance(perception, bool) or perception is None:
            return "none", False

        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        px, py = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]

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
            return self.ProcesaMovimiento(intencion, perception, True)
        else:
            return self.ProcesaMovimiento(intencion, perception, False)

    def Transit(self, perception, map):
        if isinstance(perception, bool) or perception is None: return AgentConsts.STATE_ATTACK

        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        px, py = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]

        # Si el jugador muere se vuelve a GTCC
        if px < 0:
            return AgentConsts.STATE_GO_CENTER 

        # Si se aleja mucho el jugador volvemos a GTCC
        distancia = abs(ax - px) + abs(ay - py)
        if distancia > 11.0:
            return AgentConsts.STATE_GO_CENTER

        return AgentConsts.STATE_ATTACK