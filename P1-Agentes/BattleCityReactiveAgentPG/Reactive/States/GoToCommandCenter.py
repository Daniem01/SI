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

        self.eje_prioritario = "Y"
        self.evasion_counter = 0
        self.evasion_direction = None      

    def Start(self, agent):
        print("Empieza estado GoToCommandCenter")

    def End(self):
        print("Fin del estado GoToCommandCenter")

    def ProcesaMovimiento(self, intencionMov, perception, alineado):
        # Obtener sensor frontal según la dirección
        sensor_frente = self.GetSensor(intencionMov)
        distancia_frente = self.GetDistSensor(intencionMov)

        # Sistema de evasión de objetos indestructibles
        # Si estamos en contador de evasión, mantener dirección salvo que haya indestructible delante
        if self.evasion_counter > 0:
            # Verificar si hay indestructible justo delante
            sensor_evasion = self.GetSensor(self.evasion_direction)
            dist_evasion = self.GetDistSensor(self.evasion_direction)
            
            if perception[sensor_evasion] in self.indestructibles and perception[dist_evasion] < 1.2:
                # Hay indestructible justo delante, girar 90 grados más
                self.evasion_direction = self.Rotate90Degrees(self.evasion_direction)
                self.evasion_counter = 5  # Reiniciar contador
            else:
                # Seguir en la dirección de evasión
                self.evasion_counter -= 1
            
            return self.evasion_direction
        
        # Si no hay contador activo, revisar si hay indestructible delante
        if perception[sensor_frente] in self.indestructibles and perception[distancia_frente] < 1.2:
            # Detectado indestructible: girar 90 grados y activar contador
            self.evasion_direction = self.Rotate90Degrees(intencionMov)
            self.evasion_counter = 5
            
            return self.evasion_direction

        # Si no hay obstáculo, continuar normalmente hacia el objetivo
        # Reset de evasión para siguiente ciclo limpio
        self.evasion_direction = None
        return intencionMov
    
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

    def Rotate90Degrees(self, direction):
        """Gira 90 grados a la derecha desde la dirección actual"""
        if direction == AgentConsts.MOVE_UP:
            return AgentConsts.MOVE_RIGHT
        elif direction == AgentConsts.MOVE_DOWN:
            return AgentConsts.MOVE_LEFT
        elif direction == AgentConsts.MOVE_RIGHT:
            return AgentConsts.MOVE_DOWN
        elif direction == AgentConsts.MOVE_LEFT:
            return AgentConsts.MOVE_UP
        return direction

    def Update(self, perception, map, agent):
        if isinstance(perception, bool) or perception is None: return "none", False

        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        cx, cy = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]

        # Calcular dirección hacia Command Center alternando ejes (Y primero, luego X)
        if self.eje_prioritario == "Y":
            # Alineación vertical: apuntar hacia cy
            if abs(ay - cy) < 0.5:
                # Alineado verticalmente, cambiar a eje horizontal
                self.eje_prioritario = "X"
                intencion = AgentConsts.MOVE_RIGHT if ax < cx else AgentConsts.MOVE_LEFT
            else:
                # Moverse verticalmente
                intencion = AgentConsts.MOVE_DOWN if ay < cy else AgentConsts.MOVE_UP
        else: 
            # Alineación horizontal: apuntar hacia cx
            if abs(ax - cx) < 0.5:
                # Alineado horizontalmente, cambiar a eje vertical
                self.eje_prioritario = "Y"
                intencion = AgentConsts.MOVE_DOWN if ay < cy else AgentConsts.MOVE_UP
            else:
                # Moverse horizontalmente
                intencion = AgentConsts.MOVE_RIGHT if ax < cx else AgentConsts.MOVE_LEFT

        # Aplicar sistema de evasión de indestructibles
        # - Si hay BRICK delante: pasa y lo rompe
        # - Si hay INDESTRUCTIBLE delante: gira 90° y evade 5 pasos
        # - Si hay otro INDESTRUCTIBLE en evasión: gira nuevamente
        accion = self.ProcesaMovimiento(intencion, perception, False)

        return accion, False

    def Transit(self, perception, map):
        if isinstance(perception, bool) or perception is None: return AgentConsts.STATE_GO_CENTER

        ax, ay = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        px, py = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]

        # Si el jugador está cerca cambiamos a modo ataque
        distancia = abs(ax - px) + abs(ay - py)
        if 0 <= px and distancia < 11.0:
            return AgentConsts.STATE_ATTACK

        return AgentConsts.STATE_GO_CENTER