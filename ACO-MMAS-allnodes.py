import random
MAXPHEROMONES = 100000
MINPHEROMONES = 1

'''
Max-min ant system (MMAS)

Added maximum and minimum pheromone amounts. Only global best or iteration
best tour deposited pheromone.
All edges are initialized to τmin and reinitialized to τmax when
nearing stagnation
'''


class Node:
   def __init__(self,name):
        self.name = name
        self.edges = []

   def rouletteWheelSimple(self):
        return random.sample(self.edges,1)[0]

   def rouletteWheel(self,visitedEdges,startNode):
          visitedNodes = [oneEdge.toNode for oneEdge in visitedEdges]
          viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes and oneEdge.toNode!=startNode]
          if not viableEdges: 
               viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes]

          allPheromones = sum([oneEdge.pheromones for oneEdge in viableEdges])
          num = random.uniform(0, allPheromones)
          s = 0
          i = 0
          selectedEdge = viableEdges[i]
          while(s<=num):
              selectedEdge = viableEdges[i]
              s += selectedEdge.pheromones
              i += 1
          return selectedEdge

   def __repr__(self):
        return self.name


class Edge:
   def __init__(self,fromNode,toNode,cost):
       self.fromNode = fromNode
       self.toNode = toNode
       self.cost = cost
       self.pheromones = MAXPHEROMONES

   def checkPheromones(self):
       if(self.pheromones>MAXPHEROMONES):
           self.pheromones = MAXPHEROMONES
       if(self.pheromones<MINPHEROMONES):
           self.pheromones = MINPHEROMONES

   def __repr__(self):
       return self.fromNode.name + "--(" + str(self.cost) + ")--" + self.toNode.name


class Greedy:
   def __init__(self):
       self.visitedEdges = []   
       self.visitedNodes = []

   def walk(self,startNode):
         currentNode = startNode
         currentEdge = None
         while(not checkAllNodesPresent(self.visitedEdges)):
             possibleEdges = [(edge.cost, edge) for edge in currentNode.edges if edge.toNode not in self.visitedNodes]
             possibleEdges.sort(key = lambda elem: elem[0]) # sort by cost which is first element of tuple
             #import pdb;pdb.set_trace()
             currentEdge = possibleEdges[0][1]
             currentNode = currentEdge.toNode
             self.visitedEdges.append(currentEdge)
             self.visitedNodes.append(currentNode)
             print(currentNode, currentEdge)


class ANT:
    def __init__(self):
        self.visitedEdges = []
    
    def walk(self,startNode):
        currentNode = startNode
        currentEdge = None
        while(not checkAllNodesPresent(self.visitedEdges)):
            currentEdge = currentNode.rouletteWheel(self.visitedEdges, startNode)
            currentNode = currentEdge.toNode 
            self.visitedEdges.append(currentEdge)


    def pheromones(self):
        currentCost = getSum(self.visitedEdges)
        if(currentCost<MAXCOST):
            score = 1000**(1-float(currentCost)/MAXCOST) # Score function

            # Added for MMAS
            global bestScore
            global bestEdges
            if(score > bestScore):
                bestScore = score
                bestEdges = self.visitedEdges
            # End Added for MMAS    
            for oneEdge in bestEdges:
                oneEdge.pheromones += score

def checkAllNodesPresent(edges):
    visitedNodes = [edge.toNode for edge in edges]
    return set(nodes).issubset(visitedNodes)

#Cost function
def getSum(edges):
    return sum(e.cost for e in edges)

def evaporate(edges):
    for edge in edges:
        edge.pheromones *= 0.99

# Make sure all pheromones is between MAX and MIN
def checkAllEdges(edges):
    for edge in edges:
        edge.checkPheromones()

a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")
e = Node("E")

nodes = [a,b,c,d,e]
edges = [
   Edge(a,b,100),
   Edge(a,c,175),
   Edge(a,d,100),
   Edge(a,e,75),
   Edge(b,c,50),
   Edge(b,d,75),
   Edge(b,e,125),
   Edge(c,d,100),
   Edge(c,e,125),
   Edge(d,e,75)]

#Make symetrical
for oneEdge in edges[:]:
   edges.append(Edge(oneEdge.toNode,oneEdge.fromNode,oneEdge.cost))
  

#Assign to nodes
for oneEdge in edges:
    for oneNode in nodes:
        if(oneEdge.fromNode==oneNode):
            oneNode.edges.append(oneEdge)

print("Greedy")
g = Greedy()
g.walk(a)
print("Cost:",sum([e.cost for e in g.visitedEdges]))



MAXCOST = getSum(edges)
bestScore = 0           # Added for MMAS
bestSolution = []       # Added for MMAS


for i in range(100000):
    evaporate(edges)
    ant = ANT()
    ant.walk(a)
    ant.pheromones()
    checkAllEdges(edges)
    #print i,getSum(ant.visitedEdges)
    print(getSum(ant.visitedEdges))


#Printing
ant = ANT()
ant.walk(a)
for edge in ant.visitedEdges:
    print(edge, edge.pheromones)                 

