from Agent.BaseAgent import BaseAgent
from StateMachine.StateMachine import StateMachine
from States.ExecutePlan import ExecutePlan
from GoalMonitor import GoalMonitor
from AStar.AStar import AStar
from MyProblem.BCNode import BCNode
from MyProblem.BCProblem import BCProblem
from States.AgentConsts import AgentConsts
from States.Attack import Attack
from States.RandomMovement import RandomMovement

class GoalOrientedAgent(BaseAgent):



    def __init__(self, id, name):
        super().__init__(id, name)
        dictionary = {
        "ExecutePlan" : ExecutePlan("ExecutePlan"),
        "Attack" : Attack("Attack"),
        "RandomMovement" : RandomMovement("RandomMovement")
        }
        
        self.stateMachine = StateMachine("GoalOrientedBehavior",dictionary,"ExecutePlan")
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False
        self.entry_from_plan = False
        self.last_player_x = -1
        self.last_player_y = -1

    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        print("Inicio del agente ")
        self.stateMachine.Start(self)
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

    #Metodo que se llama en cada actualización del agente, y se proporciona el vector de percepciones
    #Devuelve la acción o el disparo si o no
    def Update(self, perception, map):
        if perception == True or perception == False:
            return 0, True

        if not self.agentInit:
            self.InitAgent(perception, map)
            self.agentInit = True

        action, shot = self.stateMachine.Update(perception, map, self)

        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor.UpdateGoals(goal3Player, GoalMonitor.GOAL_PLAYER)

        exitGoal = self._CreateExitGoal(perception)
        self.goalMonitor.finalGoal = exitGoal

        if self.goalMonitor.NeedReplaning(perception, map, self):
            self.problem.InitMap(map)
            self.plan = self._CreatePlan(perception, map)

        return action, shot
    
    def _CreatePlan(self,perception,map):
        if self.goalMonitor != None:
            # seleccionamos la meta mas util ahora mismo
            currentGoal = self.goalMonitor.SelectGoal(perception, map, self)
            # nodo inicial es el nodo en el q estamos ahora
            initialNode = self._CreateInitialNode(perception)
            
            # le decimos al problema cual es el inicio y la meta
            self.problem.SetInitial(initialNode)
            self.problem.SetGoal(currentGoal)

            # guardo por si acaso
            self.plan = self.aStar.GetPlan()

            # calcular el plan con A*
            return self.plan
        
        return []
        
    @staticmethod
    def CreateNodeByPerception(perception, value, perceptionID_X, perceptionID_Y,ySize):
        xMap, yMap = BCProblem.WorldToMapCoord(perception[perceptionID_X],perception[perceptionID_Y],ySize)
        newNode = BCNode(None,BCProblem.GetCost(value),value,xMap,yMap)
        return newNode

    def _CreatePlayerGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.PLAYER,AgentConsts.PLAYER_X,AgentConsts.PLAYER_Y,15)

    def _CreateExitGoal(self,perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.EXIT,AgentConsts.EXIT_X,AgentConsts.EXIT_Y,15)
    
    def _CreateLifeGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.LIFE,AgentConsts.LIFE_X,AgentConsts.LIFE_Y,15)
    
    def _CreateInitialNode(self, perception):
        node = GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.NOTHING,AgentConsts.AGENT_X,AgentConsts.AGENT_Y,15)
        node.SetG(0)
        node.SetH(0)
        return node
    
    def _CreateDefaultGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.COMMAND_CENTER,AgentConsts.COMMAND_CENTER_X,AgentConsts.COMMAND_CENTER_Y,15)
    
    #no podemos iniciarlo en el start porque no conocemos el mapa ni las posiciones de los objetos
    def InitAgent(self,perception,map):
        #creamos el problema
        #creamos el problema
        # inicializamos:
        # - creamos el problema con BCProblem
        # - inicializamos el mapa problem.InitMap
        # - inicializamos A*
        # - creamos un plan inicial
        
        # creamos el problema con el tamaño del mapa (15x15)
        initialNode = self._CreateInitialNode(perception)
        goal1CommanCenter = self._CreateDefaultGoal(perception)
        self.problem = BCProblem(initialNode, goal1CommanCenter, 15, 15)

         # inicializamos el mapa y el algoritmo A*
        self.problem.InitMap(map)
        self.aStar = AStar(self.problem)

        goal2Life = self._CreateLifeGoal(perception)
        goal3Player = self._CreatePlayerGoal(perception)
        exitGoal = self._CreateExitGoal(perception)
        self.goalMonitor = GoalMonitor(self.problem,[goal1CommanCenter,goal2Life,goal3Player],exitGoal)

        #creamos el plan inicial
        self.plan = self._CreatePlan(perception, map)

    @staticmethod
    def ShowPlan(plan):
        for n in plan:
            print("X: ",n.x,"Y:",n.y,"[",n.value,"]{",n.G(),"} => ")

    def GetPlan(self):
        return self.plan
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        super().End(win)
        self.stateMachine.End()