import random
import json
import math
MAXPHEROMONES = 100000
MINPHEROMONES = 1


class Node:
   def __init__(self, name):
        self.name = name
        self.edges = []

   def rouletteWheelSimple(self):
        return random.sample(self.edges, 1)[0]

   def rouletteWheel(self, visitedEdges, startNode, endNode):
          visitedNodes = [oneEdge.toNode for oneEdge in visitedEdges]
          viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes and oneEdge.toNode != startNode and oneEdge.toNode != endNode]
          if not viableEdges:
               viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes]

          allPheromones = sum([oneEdge.pheromones for oneEdge in viableEdges])
          num = random.uniform(0,allPheromones)
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
   def __init__(self, fromNode, toNode, cost):
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


# haversine
def getDistance(coord1, coord2):
    
    R = 6372800  # Earth radius in meters
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    #lat1, lon1 = coord1
    #lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    distance_in_meter = 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    kilometers = distance_in_meter / 1000
    
    return kilometers


def initGraph():

  nodes = []
  edges = []

  with open('norgesbyer.json') as f:
      cities = json.load(f)

  # Create list of nodes
  for k in cities.keys():
    nodes.append( Node(k) )

  # Create list of edges
  for city1 in nodes:
    for city2 in nodes:
      if city1.name == city2.name:
        continue
      else:
        edges.append(Edge( city1, city2, getDistance(cities[city1.name], cities[city2.name]) ))
  
  #Assign edges to nodes
  for oneEdge in edges:
      for oneNode in nodes:
          if(oneEdge.fromNode == oneNode):
              oneNode.edges.append(oneEdge)

  return nodes, edges

nodes, edges = initGraph()


def checkAllNodesPresent(edges):
    visitedNodes = [edge.toNode for edge in edges]
    return set(nodes).issubset(visitedNodes)


#Cost function
def getSum(edges):
    return sum(e.cost for e in edges)
MAXCOST = getSum(edges)
bestScore = 0
bestSolution = []


class ANT:
    def __init__(self):
        self.visitedEdges = []
    
    def walk(self, startNodeName, endNodeName, nodes):
        for n in nodes:
          if n.name == startNodeName:
            startNode = n
            currentNode = n
            currentEdge = None
          if n.name == endNodeName:
            endNode = n

        counter = 10
        while(counter > 0):
            currentEdge = currentNode.rouletteWheel(self.visitedEdges, startNode, endNode)
            currentNode = currentEdge.toNode 
            self.visitedEdges.append(currentEdge)
            counter = counter - 1

        for edge in currentNode.edges:
          if edge.fromNode == currentNode and edge.toNode.name == endNodeName:
            self.visitedEdges.append(edge)


    def pheromones(self):
        currentCost = getSum(self.visitedEdges)
        if(currentCost < MAXCOST):
            score = 1000**(1-float(currentCost) / MAXCOST) # Score function
            global bestScore
            global bestEdges
            if(score > bestScore):
                bestScore = score
                bestEdges = self.visitedEdges
            for oneEdge in bestEdges:
                oneEdge.pheromones += score


def evaporate(edges):
    for edge in edges:
        edge.pheromones *= 0.99


def checkAllEdges(edges):
    for edge in edges:
        edge.checkPheromones()


for i in range(100000):
    evaporate(edges)
    ant = ANT()
    ant.walk("a", "al", nodes)
    ant.pheromones()
    checkAllEdges(edges)
    #print i,getSum(ant.visitedEdges)
    print(getSum(ant.visitedEdges))


#Printing
ant = ANT()
ant.walk("a", "al", nodes)
for edge in ant.visitedEdges:
    print(edge, edge.pheromones)
