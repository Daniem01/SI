import random
from States.AgentConsts import AgentConsts

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

    def ForceToRecalculate(self):
        self.recalculate = True

    def NeedReplaning(self, perception, map, agent):
        if self.recalculate:
            self.lastTime = perception[AgentConsts.TIME]
            return True

        # replanifico cada 50 uds de tiempo(50 de momento, ir viendo q funciona mejor luego)
        currentTime = perception[AgentConsts.TIME]
        if currentTime - self.lastTime > 50:
            self.lastTime = currentTime
            return True
        
        # replanificamos tb si tenemos poca vida (1 o menos)
        if perception[AgentConsts.HEALTH] <= 1:
            self.lastTime = currentTime
            return True
        
        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        # si tiene poca vida y existe el power up de vida, vamos a por el
        if perception[AgentConsts.HEALTH] <= 1 and self.goals[GoalMonitor.GOAL_LIFE] is not None:
            return self.goals[GoalMonitor.GOAL_LIFE]
        
        # si existe el comand center vamos a por el
        if self.goals[GoalMonitor.GOAL_COMMAND_CENTRER] is not None:
            return self.goals[GoalMonitor.GOAL_COMMAND_CENTRER]
        
        # si no, perseguimos al jugador
        if self.goals[GoalMonitor.GOAL_PLAYER] is not None:
            return self.goals[GoalMonitor.GOAL_PLAYER]

        # meta aleatoria de las disponibles como ultimo recurso
        return self.goals[random.randint(0,len(self.goals))]
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
