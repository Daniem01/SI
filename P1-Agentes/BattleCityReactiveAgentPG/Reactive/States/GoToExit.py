from StateMachine.State import State
from States.AgentConsts import AgentConsts

class GoToExit(State):

    def __init__(self, id):
        super().__init__(id)
        self.indestructibles = [
            AgentConsts.UNBREAKABLE,
            AgentConsts.SEMI_UNBREKABLE,
            AgentConsts.OTHER,
        ]
        self.eje_prioritario = "Y"
        self.evasion_counter = 0
        self.evasion_direction = None
        self.stuck_counter = 0
        self.last_pos = None
      
        # Mapeos para sensores
        self.sensor_map = {
            AgentConsts.MOVE_UP: AgentConsts.NEIGHBORHOOD_UP,
            AgentConsts.MOVE_DOWN: AgentConsts.NEIGHBORHOOD_DOWN,
            AgentConsts.MOVE_LEFT: AgentConsts.NEIGHBORHOOD_LEFT,
            AgentConsts.MOVE_RIGHT: AgentConsts.NEIGHBORHOOD_RIGHT,
        }
        self.dist_sensor_map = {
            AgentConsts.MOVE_UP: AgentConsts.NEIGHBORHOOD_DIST_UP,
            AgentConsts.MOVE_DOWN: AgentConsts.NEIGHBORHOOD_DIST_DOWN,
            AgentConsts.MOVE_LEFT: AgentConsts.NEIGHBORHOOD_DIST_LEFT,
            AgentConsts.MOVE_RIGHT: AgentConsts.NEIGHBORHOOD_DIST_RIGHT,
        }
        self.rotation_map = {
            AgentConsts.MOVE_UP: AgentConsts.MOVE_RIGHT,
            AgentConsts.MOVE_DOWN: AgentConsts.MOVE_LEFT,
            AgentConsts.MOVE_RIGHT: AgentConsts.MOVE_DOWN,
            AgentConsts.MOVE_LEFT: AgentConsts.MOVE_UP,
        }      

    def Start(self, agent):
        print("Empieza estado GoToExit")

    def End(self):
        print("Fin del estado GoToExit")

    def GetSensor(self, action):
        # Devuelve el índice del sensor de vecindad
        if action == AgentConsts.MOVE_UP:    return AgentConsts.NEIGHBORHOOD_UP
        if action == AgentConsts.MOVE_DOWN:  return AgentConsts.NEIGHBORHOOD_DOWN
        if action == AgentConsts.MOVE_LEFT:  return AgentConsts.NEIGHBORHOOD_LEFT
        if action == AgentConsts.MOVE_RIGHT: return AgentConsts.NEIGHBORHOOD_RIGHT
        return AgentConsts.NEIGHBORHOOD_UP

    def GetDistSensor(self, action):
        # Devuelve el índice de la distancia del sensor 
        if action == AgentConsts.MOVE_UP:    return AgentConsts.NEIGHBORHOOD_DIST_UP
        if action == AgentConsts.MOVE_DOWN:  return AgentConsts.NEIGHBORHOOD_DIST_DOWN
        if action == AgentConsts.MOVE_LEFT:  return AgentConsts.NEIGHBORHOOD_DIST_LEFT
        if action == AgentConsts.MOVE_RIGHT: return AgentConsts.NEIGHBORHOOD_DIST_RIGHT
        return AgentConsts.NEIGHBORHOOD_DIST_UP
    
    def Rotate90Degrees(self, direction):
        # Gira 90 grados en sentido horario desde la dirección actual para evasiones
        if direction == AgentConsts.MOVE_UP:
            return AgentConsts.MOVE_RIGHT
        elif direction == AgentConsts.MOVE_RIGHT:
            return AgentConsts.MOVE_DOWN
        elif direction == AgentConsts.MOVE_DOWN:
            return AgentConsts.MOVE_LEFT
        elif direction == AgentConsts.MOVE_LEFT:
            return AgentConsts.MOVE_UP
        return direction

    def ProcesaMovimiento(self, intencionMov, perception):
        # Si estamos en una evasion la terminamos
        if self.evasion_counter > 0:
            self.evasion_counter -= 1
            # Comprobamos si el camino de evasión se ha bloqueado de repente
            sensor_ev = self.GetSensor(self.evasion_direction)
            distancia_ev = self.GetDistSensor(self.evasion_direction)
            
            if perception[sensor_ev] in self.indestructibles and perception[distancia_ev] < 1.2:
                # Si el escape también se bloquea, giramos 180 grados más
                self.evasion_direction = self.Rotate90Degrees(self.Rotate90Degrees(self.evasion_direction))
                self.evasion_counter = 12
            
            accion_final = self.evasion_direction
        
        else:
            # Si no hay evasión miramos si la intención de movimiento está bloqueada por un indestructible
            sensorf = self.GetSensor(intencionMov)
            distanciaf = self.GetDistSensor(intencionMov)

            if perception[sensorf] in self.indestructibles and perception[distanciaf] < 1.2:
                # Si detectamos un indestuctrible hacemos una evasión inteligente
                self.evasion_direction = self.Rotate90Degrees(intencionMov)
                self.evasion_counter = 12  # 12 pasos para esquivar el obstáculo y volver al camino
                
                accion_final = self.evasion_direction
            else:
                # El camino está libre de objetos indestructibles -> seguimos con la intención original
                accion_final = intencionMov

        # Logica de disparo
        sensor_final = self.GetSensor(accion_final)
        disparar = (perception[sensor_final] == AgentConsts.BRICK)

        return accion_final, disparar
    
    def ChooseBestEvationDirection(self, intencionMov, ax, ay, cx, cy):
        if intencionMov in (AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN):
            # Si estoy bloqueado en vertical, miro si el águila está a la derecha o izquierda
            return AgentConsts.MOVE_RIGHT if ax < cx else AgentConsts.MOVE_LEFT
        else:
            # Si estoy bloqueado en horizontal, miro si el águila está arriba o abajo
            return AgentConsts.MOVE_DOWN if ay < cy else AgentConsts.MOVE_UP

    def Update(self, perception, map, agent):
        if isinstance(perception, bool) or perception is None:
            return "none", False
        
        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        cx, cy = perception[AgentConsts.EXIT_X], perception[AgentConsts.EXIT_Y]
        step_threshold = 1.2 # Margen de alineamiento para considerar que estamos en el eje correcto

        # Comparamos la posición actual con la anterior para detectar si estamos atascados
        if self.last_pos is not None:
            if abs(self.last_pos[0] - ax) < 0.05 and abs(self.last_pos[1] - ay) < 0.05:
                self.stuck_counter += 1
            else:
                self.stuck_counter = 0
        self.last_pos = (ax, ay)

        # Logica de alineamiento
        if self.eje_prioritario == "X":
            if abs(ax - cx) > step_threshold:
                intencion = AgentConsts.MOVE_RIGHT if ax < cx else AgentConsts.MOVE_LEFT
            else:
                self.eje_prioritario = "Y"
                intencion = AgentConsts.MOVE_UP if ay < cy else AgentConsts.MOVE_DOWN
        else: # Prioridad Y
            if abs(ay - cy) > step_threshold:
                intencion = AgentConsts.MOVE_UP if ay < cy else AgentConsts.MOVE_DOWN
            else:
                self.eje_prioritario = "X"
                intencion = AgentConsts.MOVE_RIGHT if ax < cx else AgentConsts.MOVE_LEFT

        # Hacemos el ProcesaMovimiento
        accion, disparo = self.ProcesaMovimiento(intencion, perception)

        # Si llevamos bloquedos 11 estados consecutivos se fuerza evasion
        if self.stuck_counter >= 11:
            self.evasion_direction = self.Rotate90Degrees(intencion)
            self.evasion_counter = 10 
            self.stuck_counter = 0
            # Devolvemos la nueva dirección y forzamos disparo para abrir camino
            return self.evasion_direction, True

        return accion, disparo

    def Transit(self, perception, map):
        if isinstance(perception, bool) or perception is None: 
            return AgentConsts.STATE_EXIT

        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        px, py = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        distancia = abs(ax - px) + abs(ay - py)

        # Si hay command center vamos a ir hacia el
        if perception[AgentConsts.COMMAND_CENTER_X] > 0:
            return AgentConsts.STATE_GO_CENTER
        # Si el jugador está cerca cambiamos a modo ataque
        elif 0 <= px and distancia < 11.0:
            return AgentConsts.STATE_ATTACK
        else:
            return AgentConsts.STATE_EXIT