
#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node
class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem #problema a resolver

    def GetPlan(self):
        findGoal = False
        #TODO implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        self.open.clear()
        self.precessed.clear()
        self.open.append(self.problem.Initial())
        path = []

         #mientras no encontremos la meta y haya elementos en open....
        while len(self.open) > 0 and not findGoal:
            
            # cogemos nodo con menor F (G+H) de la lista open
            current = min(self.open, key=lambda node: node.GetF())
            self.open.remove(current)
            
            # es la meta?
            if self.problem.IsGoal(current):
                findGoal = True
                path = self.ReconstructPath(current)
                break
            
            # marco como procesado
            self.precessed.append(current)
            
            # getteamos sus sucesores (casillas vecinas accesibles)
            successors = self.problem.GetSucessors(current)
            
            # si no hay sucesores, no hay solucion
            if len(successors) == 0:
                return []
            
            for successor in successors:
                # si ya fue procesado  lo ignoramos
                if successor in self.precessed:
                    continue
                
                # calculamos nuevo coste G para llegar a este sucesor
                newG = current.GetG() + self.problem.GetCost(successor.GetValue())
                
                # compruebo si esta ya en open
                inOpen = self.GetSucesorInOpen(successor)
                
                if inOpen is None:
                    # si no esta en open,lo configuramos y añadimos
                    self._ConfigureNode(successor, current, newG)
                    self.open.append(successor)
                else:
                    # si esta en open, ha encontrado un camino mas barato?
                    if newG < inOpen.GetG():
                        # actualizamos padre y coste
                        self._ConfigureNode(inOpen, current, newG)

        # si no encontramos la meta devolvemos path vacio
        if not findGoal:
            return []
        
        return path
    

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        # Seteamos la heuristica
        node.SetH(self.problem.Heuristic(node))


    def ApendInOpen(self, node):
        if node.g == None:
            print("ApendInOpen ", node.x, node.y)
        self.open.append(node)

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found

    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        current = goal
        # Devolvemos el path invertido desde la meta hasta que el padre sea None.
        while current is not None:
            path.append(current)
            current = current.parent

        # Tenemos la ruta pero Meta -> Inicio asi que se tiene que invertir [::-1]
        return path[::-1]



