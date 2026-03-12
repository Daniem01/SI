from StateMachine.State import State
from States.AgentConsts import AgentConsts

class GoToCommandCenter(State):

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

    def Start(self, agent):
        print("Empieza estado GoToCommandCenter")

    def End(self):
        print("Fin del estado GoToCommandCenter")

    def ProcesaMovimiento(self, intencionMov, perception, alineado):
        # debug log
        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        cx, cy = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]
        print(f"GTCC ProcesaMovimiento pos=({ax:.1f},{ay:.1f}) inten={intencionMov} last={self.last_action} stuck={self.stuck_count}")
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
        # Up
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
        # Left
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

        # Lógica de disparo
        # Solo disparamos si hay un ladrillo delante
        disparar = alineado or (perception[sensor_frente] == AgentConsts.BRICK)

        # Si hay un bloque indestructible directamente en frente, cambiamos
        if perception[sensor_frente] in self.indestructibles:
            print("GTCC detected indestructible in front", perception[sensor_frente])
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
                # Todas las direcciones bloqueadas: gira derecha por defecto
                # fallback rotate through other directions when stuck
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
        
        # cuando el frente está libre, limpiamos avoid_direction
        if self.avoid_direction is not None and perception[sensor_frente] not in self.indestructibles:
            self.avoid_direction = None

        self.last_action = intencionMov
        return intencionMov, disparar

    def Update(self, perception, map, agent):
        if isinstance(perception, bool) or perception is None:
            return "none", False

        # Como hay decimales es dificil que sea exactas ciertas comparaciones con las posiciones asi que usamos aproximaciones
        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        cx, cy = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]
        
        # Reducimos primero una distancia, X o Y para luego poder ir recto destruyendo
        if abs(ax - cx) > abs(ay - cy):
            intencion = AgentConsts.MOVE_RIGHT if ax < cx else AgentConsts.MOVE_LEFT
        else:
            intencion = AgentConsts.MOVE_DOWN if ay < cy else AgentConsts.MOVE_UP

        # False al disparar porque el procesaMovimiento vera cuando es oportuno disparar   
        return self.ProcesaMovimiento(intencion, perception, False)

    def Transit(self, perception, map):
        if isinstance(perception, bool) or perception is None: return AgentConsts.STATE_GO_CENTER

        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        px, py = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]

        # Si el jugador está cerca cambiamos a modo ataque
        distancia = abs(ax - px) + abs(ay - py)
        if 0 <= px and distancia < 11.0:
            return AgentConsts.STATE_ATTACK

        return AgentConsts.STATE_GO_CENTER