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
        
        
    def valideaza(self):
        matrDesfasuarata = self.startNode[0] + self.startNode[1] + self.startNode[2]
        inv = 0
        for i,placuta in enumerate(matrDesfasuarata):
            for placuta2 in matrDesfasuarata[i+1:]:
                if placuta > placuta2 and placuta2:
                    inv+=1
                    
        return inv%2==0

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
            
    def succesori(self, node,euristica):
        lsucc = []
        
        for lGol in range(3):
            gasit = False
            for cGol in range(3):
                if node.value[lGol][cGol] == 0:
                    
                    gasit = True
                    break
                
            if gasit:
                break
            
        directii = [[-1,0],[1,0],[0,-1],[0,1]]
            
            
        for d in directii:
            lPlacuta = lGol+d[0]
            cPlacuta = cGol+d[1]
            if not (0<=lPlacuta<=2 and 0<=cPlacuta<=2):
                continue 
            infoSuccesor = copy.deepcopy(node.value)
            infoSuccesor[lGol][cGol],infoSuccesor[lPlacuta][cPlacuta] = infoSuccesor[lPlacuta][cPlacuta], infoSuccesor[lGol][cGol]     
                

            if not node.inDrum(infoSuccesor):
                lsucc.append(Node(infoSuccesor, node.g+1, self.estimeaza_h(infoSuccesor,euristica),node))
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
      
      
      
            
def a_star(graph : Graph ,euristica, nsol = 1):
    
    if not graph.valideaza():
        return 0
    
    open = [Node(graph.startNode)]
    closed = []
    
    while open:
        curr = open.pop(0)
        if graph.scop(curr.value):
            print(repr(curr))
            nsol -= 1
            if nsol == 0:
                return

        succesori = graph.succesori(curr,euristica)
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
            

f = open("input5.txt", "r")
continut = f.read()
start = [list(map(int,linie.strip().split())) for linie in continut.strip().split('\n')]  
scopuri = [[1,2,3],
           [4,5,6],
           [7,8,0]       
]



g = Graph(start,scopuri)
a_star(g,"banala",1)

         

