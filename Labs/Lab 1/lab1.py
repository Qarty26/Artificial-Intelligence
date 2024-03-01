class Node:
    def __init__(self, value, parent = None):
        self.value=value
        self.parent=parent
        
        
    def drumRadacina(self):
        node = self
        lDrum = []
        while node:
            lDrum.append(node)
            node = node.parent
            
        return lDrum[::-1]
    
    
    def inDrum(self,nodeValue):
        node = self
        while node:
            if node.value == nodeValue:
                return True
            node = node.parent
        return False
    
   
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return "{} ({})".format(str(self.value), "->".join([str(x) for x  in self.drumRadacina()]))



class Graph:
    def __init__(self, matrix, startNode, endNodes):
        self.matrix = matrix
        self.startNode = startNode
        self.endNodes = endNodes

    def scop(self, nodeValue):
        return nodeValue in self.endNodes

    def succesori(self, node):
        lsucc = []
        for valueSuccesor in range(len(self.matrix)):
            if self.matrix[node.value][valueSuccesor] == 1 and not node.inDrum(valueSuccesor):
                lsucc.append(Node(valueSuccesor,node))
        return lsucc



def bfs(graph, nsol=4):
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
        
def dfs(graph, node, nsol = 0):
    
    if graph.scop(node.value):
        print(repr(node))
        nsol-=1
        return nsol
    
    succesori = graph.succesori(node)
    for s in succesori:
        if nsol > 0:
            nsol = dfs(graph,s,nsol)
            
    return nsol
    
        

m = [
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
]

start = 0
ends = [5,9]

graf = Graph(m, start, ends)
bfs(graf, 9)
print("======================")
dfs(graf, Node(0),5)
