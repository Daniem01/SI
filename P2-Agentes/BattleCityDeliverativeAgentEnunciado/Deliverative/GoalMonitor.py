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
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True

        currentTime = perception[AgentConsts.TIME]

        if currentTime - self.lastTime > 4.5:
            self.lastTime = currentTime
            return True

        if perception[AgentConsts.HEALTH] <= 1:
            self.lastTime = currentTime
            return True

        cc_alive = not (
            perception[AgentConsts.COMMAND_CENTER_X] == -1 and
            perception[AgentConsts.COMMAND_CENTER_Y] == -1
        )

        # solo persigo cambios del player cuando el CC ya no existe
        if not cc_alive:
            px = perception[AgentConsts.PLAYER_X]
            py = perception[AgentConsts.PLAYER_Y]
            if px != agent.last_player_x or py != agent.last_player_y:
                agent.last_player_x = px
                agent.last_player_y = py
                self.lastTime = currentTime
                return True

        return False

    def SelectGoal(self, perception, map, agent):
        cc_alive = not (
            perception[AgentConsts.COMMAND_CENTER_X] == -1 and
            perception[AgentConsts.COMMAND_CENTER_Y] == -1
        )

        if not cc_alive:
            self.goals[GoalMonitor.GOAL_COMMAND_CENTRER] = None

        if perception[AgentConsts.HEALTH] <= 1 and self.goals[GoalMonitor.GOAL_LIFE] is not None:
            return self.goals[GoalMonitor.GOAL_LIFE]

        # prioridad 1: CC
        if cc_alive and self.goals[GoalMonitor.GOAL_COMMAND_CENTRER] is not None:
            return self.goals[GoalMonitor.GOAL_COMMAND_CENTRER]

        # prioridad 2: salida, solo cuando el CC ya no existe
        if not cc_alive and self.finalGoal is not None:
            return self.finalGoal

        # prioridad 3: player
        if self.goals[GoalMonitor.GOAL_PLAYER] is not None:
            return self.goals[GoalMonitor.GOAL_PLAYER]

        return None

    def UpdateGoals(self, goal, goalId):
        self.goals[goalId] = goal