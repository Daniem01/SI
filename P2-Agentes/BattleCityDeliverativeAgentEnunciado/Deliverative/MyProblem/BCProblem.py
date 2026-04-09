#import sys
#sys.path.insert(1, '../AStar')
from AStar.Problem import Problem
from MyProblem.BCNode import BCNode
from States.AgentConsts import AgentConsts
import sys
import numpy as np


class BCProblem(Problem):
    

    def __init__(self, initial, goal, xSize, ySize):
        super().__init__(initial, goal)
        self.map = np.zeros((xSize,ySize),dtype=int)
        self.xSize = xSize
        self.ySize = ySize
    
    def InitMap(self,m):
        for i in range(len(m)):
            x,y = BCProblem.Vector2MatrixCoord(i,self.xSize,self.ySize)
            self.map[x][y] = m[i]
    
    #Muestra el mapa por consola
    def ShowMap(self):
        for j in range(self.ySize):
            s = ""
            for i in range(self.xSize):
                s += ("[" + str(i) + "," + str(j) + "," + str(self.map[i][j]) +"]")
            print(s)

    #Calcula la heuristica del nodo en base al problema planteado
    def Heuristic(self, node):
        # Si no hay objetivo devolvemos 0
        if self.goal is None:
            return 0
        # Usamos la Distancia de Manhattan
        dist_x = abs(node.x - self.goal.x)
        dist_y = abs(node.y - self.goal.y)
        return dist_x + dist_y

    #Genera la lista de sucesores del nodo (Se necesita reimplementar)
    def GetSucessors(self, node):
        successors = []
        direcciones = [(1,0), (-1,0),(0,1), (0,-1)] # Direcciones posibles

        for dx, dy in direcciones:
            # Calulamos la posicion que tendra despues del movimiento para ver si es una posicion valida
            nx, ny = node.x + dx, node.y + dy

            if 0 <= nx < self.xSize and 0 <= ny < self.ySize:
                casilla = self.map[nx][ny]
                # Si te puedes mover hacia esa casilla creamos un nodo y lo metemos en sucessors como camino posible
                if BCProblem.CanMove(casilla):
                    self.CreateNode(successors, node, nx, ny)

        return successors
    
    #métodos estáticos
    #nos dice si podemos movernos hacia una casilla, se debe poner el valor de la casilla como
    #parámetro
    @staticmethod
    def CanMove(value):
        return value != AgentConsts.UNBREAKABLE and value != AgentConsts.SEMI_UNBREKABLE
    
    #convierte coordenadas mapa en formato vector a matriz
    @staticmethod
    def Vector2MatrixCoord(pos,xSize,ySize):
        x = pos % xSize
        y = pos // ySize #division entera
        return x,y

    #convierte coordenadas mapa en formato matriz a vector
    @staticmethod
    def Matrix2VectorCoord(x,y,xSize):
        return y * xSize + x
    
    #convierte coordenadas del entorno (World) en coordenadas mapa (nótese que la Y está invertida)
    @staticmethod
    def MapToWorldCoord(x,y,ySize):
        xW = x * 2
        yW = (ySize - y - 1) * 2
        return xW, yW
    
    #convierte coordenadas del entorno (World) en coordenadas mapa (nótese que la Y está invertida)
    @staticmethod
    def WorldToMapCoord(xW,yW,ySize):
        x = xW // 2
        y = yW // 2
        y = ySize - y - 1
        return x, y
    
    #versión real del método anterior, que nos ayuda a buscar los centros de las celdas.
    #aqui nos dirá los decimales, es decir como de cerca estamos de la esquina superior derecha
    #un valor de 1.9,1.9 nos dice que estamos en la casilla 1,1 muy cerca de la 2,2
    #en realidad, lo que buscamos es el punto medio de la casilla, es decir la 1.5, 1.5 en el caso
    #de la casilla 1,1
    @staticmethod
    def WorldToMapCoordFloat(xW,yW,ySize):
        x = xW / 2
        invY = (ySize*2) - yW
        invY = invY / 2
        #invY = invY - 1
        return x, invY

    #crea un nodo y lo añade a successors (lista) con el padre indicado y la posición x,y en coordenadas mapa 
    @staticmethod
    def GetCost(value):
        # Damos un coste a cada tipo de casilla del mapa.
        if value is AgentConsts.NOTHING:
            return 1
        elif value is AgentConsts.BRICK: # Consideramos que romper el bloque es 3 veces mas costoso que ir por un camino normal
            return 3
        elif value is AgentConsts.SEMI_BREKABLE: # Consideramos que romper este bloque es 5 veces mas costoso que ir por un camino normal
            return 5         
        elif value is AgentConsts.UNBREAKABLE:
            return sys.maxsize
        elif value is AgentConsts.SEMI_UNBREKABLE:
            return sys.maxsize
        elif value is AgentConsts.COMMAND_CENTER:
            return 1
        elif value is AgentConsts.LIFE:
            return 1
        else:
            return sys.maxsize
    
    def CreateNode(self,successors,parent,x,y):
        value=self.map[x][y]
        g=BCProblem.GetCost(value)
        rightNode = BCNode(parent,g,value,x,y)
        rightNode.SetH(self.Heuristic(rightNode))
        successors.append(rightNode)

    #Calcula el coste de ir del nodo from al nodo to (Se necesita reimplementar)
    def GetGCost(self, nodeTo):
        return BCProblem.GetCost(nodeTo.value)