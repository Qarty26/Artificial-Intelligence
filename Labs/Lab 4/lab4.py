from queue import PriorityQueue
import copy 

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
    
    def __le__(self, other):
        return self.f < other.f or (self.f == other.f and self.g >= other.g)

    def __lt__(self, other):
        return self.f < other.f or (self.f == other.f and self.g > other.g)

    def __gt__(self, other):
        return self.f > other.f or (self.f == other.f  and self.g < other.g)

   
    def __str__(self):
        return f"({str(self.value)}, g:{self.g},f:{self.f})"
    
    def __repr__(self):
        return "{} ({})".format(str(self.value), "->".join([str(x) for x  in self.drumRadacina()]))



class Graph:
    def __init__(self, startNode, endNodes):
        self.startNode = startNode
        self.endNodes = endNodes

    def scop(self, nodeValue):
        return nodeValue in self.endNodes
    
    def estimeaza_h(self, info_nod, euristica):
        if self.scop(info_nod):
            return 0
        if euristica == "banala":
            return 1
        if euristica == "euristica mutari":
            minH = float('inf')
            for scop in self.endNodes:
                h=0
                for istiva, stiva in enumerate(scop):
                    for ibloc, bloc in enumerate(stiva):
                        try:
                            if info_nod[istiva][ibloc]!=bloc:
                                h+=1    
                        except:
                             h+=1
            return minH
            
    def succesori(self, node):
        lsucc = []
        for i,stiva in enumerate(node.value):
            if not stiva:
                continue
            
            copyStive = copy.deepcopy(node.value)
            bloc = copyStive[i].pop()
            
            for j in range(len(node.value)):
                if i == j:
                    continue
                infoSuccesor = copy.deepcopy(copyStive)
                infoSuccesor[j].append(bloc)
                

            if not node.inDrum(infoSuccesor):
                lsucc.append(Node(infoSuccesor, node.g+1, self.estimeaza_h(infoSuccesor,"banala"),node))
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
        
        
        
def bin_search(listaNoduri, nodNou, ls, ld):
    if len(listaNoduri)==0:
        return 0
    
    if ls==ld:
        if nodNou<listaNoduri[ls]:
            return ls
        else:
            return ld+1
        
    else:
        mij=(ls+ld)//2
        
        if nodNou<listaNoduri[ls]:
            return bin_search(listaNoduri, nodNou, ls, mij)
        else:
            return bin_search(listaNoduri, nodNou, mij+1, ld)



def aStarSolMultiple2(graph, nsol=1):
    queue = [Node(graph.startNode)]
    while queue:
        curr = queue.pop(0)
        if graph.scop(curr.value):
            print(repr(curr))
            nsol -= 1
            if nsol == 0:
                return
        succes = graph.succesori(curr)
        
        for suc in succes: 
            insert_index = bin_search(queue, suc,0,len(queue)-1)
            queue.insert(insert_index, suc)
        
        
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
            
def a_star(graph : Graph , nsol = 1):
    open = [Node(graph.startNode)]
    closed = []
    
    while open:
        curr = open.pop(0)
        if graph.scop(curr.value):
            print(repr(curr))
            nsol -= 1
            if nsol == 0:
                return

        succesori = graph.succesori(curr)
        closed.append(curr)
        
        for s in succesori:
            newNode = None
            if not curr.inDrum(s.value):
                
                if s in open:
                    indexNode = open.index(s)

                    if s.f < open[indexNode].f or (s.f == open[indexNode].f and s.g > open[indexNode].g):
                        open.pop(indexNode)
                        s.parent = curr
                        s.g += curr.g
                        s.h = graph.estimeaza_h(s.value)
                        s.f = s.g + s.h
                        newNode = s
                        
                if s in closed:
                    indexNode = closed.index(s)

                    if s.f < closed[indexNode].f or (s.f == closed[indexNode].f and s.g > closed[indexNode].g):
                        closed.pop(indexNode)
                        s.parent = curr
                        s.g += curr.g
                        s.h = graph.estimeaza_h(s.value)
                        s.f = s.g + s.h
                        newNode = s
                else:
                    newNode = s

                if newNode is not None:
                    open.append(newNode)
                    open.sort()
            
def calculeazaStive(sir):
    return [linie.strip().split() if linie!='#' else [] for linie in sir.strip().split('\n')]
    
f = open("input.txt", "r")
sirStart, sirScopuri = f.read().split("=========")  

start = calculeazaStive(sirStart)
scopuri = [calculeazaStive(x) for x in sirScopuri.split("---")]  



g = Graph(start,scopuri)
a_star(g,4)
        
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
                
        

#todo: blocuri verificare (subpunctul b)


