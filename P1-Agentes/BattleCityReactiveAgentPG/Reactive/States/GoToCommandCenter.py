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
        self.eje_prioritario = "Y"
        self.avoid_steps = 0
        self.avoid_direction = None
        self.prev_pos = None      
        self.stuck_count = 0
        self.emergency_mode_steps = 0
        self.last_stuck_direction = None
        self.persist_escape_steps = 0
        self.escape_direction_locked = None      

    def Start(self, agent):
        print("Empieza estado GoToCommandCenter")

    def End(self):
        print("Fin del estado GoToCommandCenter")

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
        # Solo disparamos si hay un ladrillo delante o estamos alineados con el jugador
        disparar = alineado or (perception[sensor_frente] == AgentConsts.BRICK)

        # Si hay un bloque indestructible directamente en frente, cambiamos
        if perception[sensor_frente] in self.indestructibles:
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
                # Todas las direcciones bloqueadas: verificar todas 4 direcciones posibles
                todas_direcciones = [AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_LEFT, AgentConsts.MOVE_RIGHT]
                alternativas_validas = []
                
                for direccion in todas_direcciones:
                    if direccion != intencionMov:
                        sensor_test = self.GetSensor(direccion)
                        dist_test = self.GetDistSensor(direccion)
                        if perception[sensor_test] not in self.indestructibles and perception[dist_test] > 1:
                            alternativas_validas.append(direccion)
                
                if alternativas_validas:
                    # Preferir dirección diferente a la anterior
                    if self.last_stuck_direction in alternativas_validas and len(alternativas_validas) > 1:
                        resultado = [d for d in alternativas_validas if d != self.last_stuck_direction][0]
                    else:
                        resultado = alternativas_validas[0]
                    self.last_stuck_direction = resultado
                else:
                    # Completamente rodeado: girar en espiral (preferencia: derecha, arriba, izquierda, abajo)
                    resultado = (accion_lado1 if accion_lado1 != intencionMov else accion_lado2)
                
                self.last_action = resultado
                self.avoid_direction = resultado
                self.avoid_steps = 2
                return resultado, disparar
        
        # cuando el frente está libre, limpiamos avoid_direction
        if self.avoid_direction is not None and perception[sensor_frente] not in self.indestructibles:
            self.avoid_direction = None

        self.last_action = intencionMov
        return intencionMov, disparar
    
    def GetSensor(self, action):
        if action == AgentConsts.MOVE_UP: return AgentConsts.NEIGHBORHOOD_UP
        if action == AgentConsts.MOVE_DOWN: return AgentConsts.NEIGHBORHOOD_DOWN
        if action == AgentConsts.MOVE_LEFT: return AgentConsts.NEIGHBORHOOD_LEFT
        if action == AgentConsts.MOVE_RIGHT: return AgentConsts.NEIGHBORHOOD_RIGHT
        return AgentConsts.NEIGHBORHOOD_UP

    def GetDistSensor(self, action):
        if action == AgentConsts.MOVE_UP: return AgentConsts.NEIGHBORHOOD_DIST_UP
        if action == AgentConsts.MOVE_DOWN: return AgentConsts.NEIGHBORHOOD_DIST_DOWN
        if action == AgentConsts.MOVE_LEFT: return AgentConsts.NEIGHBORHOOD_DIST_LEFT
        if action == AgentConsts.MOVE_RIGHT: return AgentConsts.NEIGHBORHOOD_DIST_RIGHT
        return AgentConsts.NEIGHBORHOOD_DIST_UP

    def Update(self, perception, map, agent):
        if isinstance(perception, bool) or perception is None: return "none", False

        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        cx, cy = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]

        if self.prev_pos is not None and abs(self.prev_pos[0] - ax) < 0.1 and abs(self.prev_pos[1] - ay) < 0.1:
            self.stuck_count += 1
        else:
            self.stuck_count = 0
            self.emergency_mode_steps = 0
        self.prev_pos = (ax, ay)

        # Si está atrapado más de 2 ciclos consecutivos, activar modo emergencia FUERZA BRUTA
        if self.stuck_count > 2:
            # Modo FUERZA BRUTA: ignorar validaciones y simplemente intentar direcciones hacia el CC
            direcciones = []
            
            # Listar todas las direcciones posibles priorizando acercamiento al CC
            if ax < cx:
                direcciones.append(AgentConsts.MOVE_RIGHT)
            if ay < cy:
                direcciones.append(AgentConsts.MOVE_DOWN)
            if ax > cx:
                direcciones.append(AgentConsts.MOVE_LEFT)
            if ay > cy:
                direcciones.append(AgentConsts.MOVE_UP)
            
            # Si por alguna razón no hay dirección válida, rotación
            if not direcciones:
                direcciones = [AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_DOWN, 
                             AgentConsts.MOVE_LEFT, AgentConsts.MOVE_UP]
            
            # Rotación cíclica a través de direcciones
            indice = self.emergency_mode_steps % len(direcciones)
            dir_intento = direcciones[indice]
            self.emergency_mode_steps += 1
            
            # Si lleva 30+ pasos intentando, resetear
            if self.emergency_mode_steps > 30:
                self.emergency_mode_steps = 0
                self.stuck_count = 0
            
            # IMPORTANTE: Devolver DIRECTAMENTE sin ProcesaMovimiento
            # Solo devolver la dirección, el motor físico manejará colisiones
            return dir_intento, False

        # Si está en evasión persistente, mantener dirección SIN procesar (evita cambios bruscos)
        if self.persist_escape_steps > 0:
            self.persist_escape_steps -= 1
            return self.escape_direction_locked, False
        else:
            # Cuando termina evasión: cambiar el eje prioritario para salir del bloqueo
            if self.escape_direction_locked is not None:
                if self.escape_direction_locked in (AgentConsts.MOVE_LEFT, AgentConsts.MOVE_RIGHT):
                    self.eje_prioritario = "X"
                else:
                    self.eje_prioritario = "Y"
            self.escape_direction_locked = None

        if self.avoid_steps > 0:
            self.avoid_steps -= 1
            return self.ProcesaMovimiento(self.avoid_direction, perception, False)

        # Miramos qué dirección nos queremos mover para acercarnos a command center
        if self.eje_prioritario == "Y":
            # Miramos la alineacion vertical
            if abs(ay - cy) < 0.5:
                self.eje_prioritario = "X"
                intencion = AgentConsts.MOVE_RIGHT if ax < cx else AgentConsts.MOVE_LEFT
            else:
                intencion = AgentConsts.MOVE_DOWN if ay < cy else AgentConsts.MOVE_UP
        else: 
            if abs(ax - cx) < 0.5:
                self.eje_prioritario = "Y"
                intencion = AgentConsts.MOVE_DOWN if ay < cy else AgentConsts.MOVE_UP
            else:
                intencion = AgentConsts.MOVE_RIGHT if ax < cx else AgentConsts.MOVE_LEFT

        # Definimos sensores y acciones según la intención
        sensor_frente = self.GetSensor(intencion)
        dist_frente = self.GetDistSensor(intencion)

        if perception[sensor_frente] in self.indestructibles and perception[dist_frente] < 1.2:
            # Obstáculo detectado: elegir dirección de escape PERPENDICULAR a la intención
            # y PERSISTIR en esa dirección para rodear eficientemente
            
            # Determinar dirección de escape PERPENDICULAR a la intención
            if intencion in (AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN):
                # Si intención es vertical, escapar horizontalmente
                escape_dir = AgentConsts.MOVE_RIGHT if ax < cx else AgentConsts.MOVE_LEFT
            else:
                # Si intención es horizontal, escapar verticalmente
                escape_dir = AgentConsts.MOVE_DOWN if ay < cy else AgentConsts.MOVE_UP
            
            # Verificar que la dirección de escape esté realmente libre
            escape_sensor = self.GetSensor(escape_dir)
            escape_dist = self.GetDistSensor(escape_dir)
            
            if perception[escape_sensor] not in self.indestructibles and perception[escape_dist] > 1:
                # Activar evasión persistente: mantener dirección 15 pasos para rodear bien
                self.escape_direction_locked = escape_dir
                self.persist_escape_steps = 15
            else:
                # Si el escape lateral está también bloqueado, usar ProcesaMovimiento para buscar alternativa
                return self.ProcesaMovimiento(intencion, perception, False)
            
            return self.ProcesaMovimiento(self.escape_direction_locked, perception, False)

        # Si no hay bloqueo seguimos hacia el command center
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