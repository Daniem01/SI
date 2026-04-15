import random
from States.AgentConsts import AgentConsts
from MyProblem.BCProblem import BCProblem

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    GOAL_EXIT = 3

    def __init__(self, problem, goals, finalGoal):
        self.goals = goals
        self.finalGoal = finalGoal
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False
        self.was_in_radius = False
        self.HUNTING_RADIUS = 6.0 

    def ForceToRecalculate(self):
        self.recalculate = True

    def IsPlayerAlive(self, perception):
        return perception[AgentConsts.PLAYER_X] != -1 and perception[AgentConsts.PLAYER_Y] != -1

    def IsCCAlive(self, perception):
        return perception[AgentConsts.COMMAND_CENTER_X] != -1 and perception[AgentConsts.COMMAND_CENTER_Y] != -1

    def IsPlayerInRadius(self, perception):
        if not self.IsPlayerAlive(perception):
            return False
        dist = self.GetDistanceToPlayer(perception)
        return dist <= self.HUNTING_RADIUS

    def NeedReplaning(self, perception, map, agent):
        if self.recalculate:
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True

        currentTime = perception[AgentConsts.TIME]

        # Comprobar umbral de tiempo
        if currentTime - self.lastTime > 4.5:
            self.lastTime = currentTime
            return True

        # El jugador ha entrado o salido del radio de caza
        in_radius = self.IsPlayerInRadius(perception)
        if not hasattr(self, 'was_in_radius'): self.was_in_radius = in_radius
        if in_radius != self.was_in_radius:
            self.was_in_radius = in_radius
            return True

        # Salud baja
        if perception[AgentConsts.HEALTH] <= 1:
            return True

        # Si el jugador o el CC han muerto el plan anterior ya no es valido
        if not self.IsCCAlive(perception) or not self.IsPlayerAlive(perception):
            return True

        return False
    
    def GetDistanceToPlayer(self, perception):
        dist_x = abs(perception[AgentConsts.AGENT_X] - perception[AgentConsts.PLAYER_X])
        dist_y = abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y])
        return (dist_x + dist_y) / 2 

    def SelectGoal(self, perception, map, agent):
        player_alive = self.IsPlayerAlive(perception)
        cc_alive = self.IsCCAlive(perception)
        
        # Si el CC ha muerto o el Jugador ha muerto ---> salida
        mission_complete = (not cc_alive) or (not player_alive)

        # Buscamos vida
        if perception[AgentConsts.HEALTH] <= 1 and self.goals[GoalMonitor.GOAL_LIFE] is not None:
            return self.goals[GoalMonitor.GOAL_LIFE]

        # Modo caza
        if self.IsPlayerInRadius(perception):
            return self.goals[GoalMonitor.GOAL_PLAYER]

        # Vamos a la salida
        if mission_complete and self.finalGoal is not None:
            return self.finalGoal

        # CC
        if cc_alive and self.goals[GoalMonitor.GOAL_COMMAND_CENTRER] is not None:
            return self.goals[GoalMonitor.GOAL_COMMAND_CENTRER]

        # Ultima opcion si no hay nada que hacer ---> cazar al jugador
        if player_alive and self.goals[GoalMonitor.GOAL_PLAYER] is not None:
            return self.goals[GoalMonitor.GOAL_PLAYER]

        return self.finalGoal
    
    def UpdateGoals(self, goal, goalId):
        self.goals[goalId] = goal