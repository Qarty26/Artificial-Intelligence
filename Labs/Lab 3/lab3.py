from queue import PriorityQueue

class Node:
    def __init__(self, value,g=0, h=0, parent = None):
        self.value=value
        self.parent=parent
        self.g = g
        self.h = h
        self.f =g + h

        
    def drumRadacina(self):
        node = self
        lDrum = [node]
        while node.parent is not None:
            node = node.parent
            lDrum.append(node)
            
        return lDrum[::-1]
    
    
    def inDrum(self,nodeValue):
        node = self
        while node is not None:
            if node.value == nodeValue:
                return True
            node = node.parent
        return False
    
    def __eq__(self, other):
        return self.g == other.g and self.f == other.f
    
    def __lt__ (self, other):
        return self.f <= other.f or (self.f==other.f and self.g > other.g)

   
    def __str__(self):
        return f"({str(self.value)}, g:{self.g},f:{self.f})"
    
    def __repr__(self):
        return "{} ({})".format(str(self.value), "->".join([str(x) for x  in self.drumRadacina()]))



class Graph:
    def __init__(self, matrix, startNode, endNodes,h):
        self.matrix = matrix
        self.startNode = startNode
        self.endNodes = endNodes
        self.h = h 

    def scop(self, nodeValue):
        return nodeValue in self.endNodes
    
    def estimeaza_h(self, info_nod):
        return self.h[info_nod]

    def succesori(self, node):
        lsucc = []
        for valueSuccesor in range(len(self.matrix)):
            if self.matrix[node.value][valueSuccesor] != 0 and not node.inDrum(valueSuccesor):
                lsucc.append(Node(valueSuccesor, node.g + self.matrix[node.value][valueSuccesor], self.estimeaza_h(valueSuccesor),node))
        return lsucc



def aStarSolMultiple(graph, nsol=1):
    queue = [Node(graph.startNode)] 
    while queue:
        curr = queue.pop(0)
        if graph.scop(curr.value):
            print(repr(curr))
            nsol -= 1
            
            if nsol == 0:
                return
          
        succes = graph.succesori(curr)
        queue += succes
        queue.sort()
        
def PQaStarSolMultiple(graph, nsol=1):
    pq = PriorityQueue()
    pq.put(Node(graph.startNode))

    while pq:
        curr = pq.get()
        if graph.scop(curr.value):
            print(repr(curr))
            nsol -= 1
            
            if nsol == 0:
                return
          
        succes = graph.succesori(curr)
        for nod in succes:
            pq.put(nod)

        
        
        
# def bfs2(graph, nsol=4):
#     queue = [Node(graph.startNode)]
#     while queue:
#         curr = queue.pop(0)
        
#         succes = graph.succesori(curr)
#         for suc in succes:
#             queue.append(suc)
        
#             if graph.scop(suc.value):
#                 print(repr(suc))
#                 nsol -= 1
#                 if nsol == 0:
#                     return

        
    
        
# def dfs(graph, node, nsol = 0):
    
#     if graph.scop(node.value):
#         print(repr(node))
#         nsol-=1
#         return nsol
    
#     succesori = graph.succesori(node)
#     for s in succesori:
#         if nsol > 0:
#             nsol = dfs(graph,s,nsol)
            
#     return nsol
 
  
# def dfs_nonrec(graph, node, nsol = 0):
#     stack = [node]
#     while stack:
#         s = stack.pop()
#         if graph.scop(s.value):
#             print(repr(s))
#             nsol-=1
#             if not nsol:
#                 return
#         stack.extend(graph.succesori(s))
                
        
m = [
        [0, 3, 5, 10, 0, 0, 100],
        [0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 4, 9, 3, 0],
        [0, 3, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 5],
        [0, 0, 3, 0, 0, 0, 0],
    ]
h=[0,1,6,2,0,3,0]

start = 0
scopuri = [4,6]

graf = Graph(m, start, scopuri, h)
aStarSolMultiple(graf, 1)
PQaStarSolMultiple(graf, 1)


