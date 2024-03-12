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
    
    
    def afisSolFisier(self, file, output):
            output = output[11:-1].split("->")
            optiuni = [
                ("(Stanga: <barca>)", "<Dreapta>"),
                ("(Stanga)", "(Dreapta: <barca>)")
            ]
            counter_optiuni = 0
            file_string = ""
            output.append("(0, 0, 0)")

            n = 0
            for i in range(len(output) - 1):
                pozitie_barca = optiuni[counter_optiuni % 2]
                numbers = output[i][1:-1].split(', ')  
                next_numbers = output[i+1][1:-1].split(', ')

                misionari = int(numbers[0])
                canibali = int(numbers[1])
                misionari_nou = int(next_numbers[0])
                canibali_nou = int(next_numbers[1])

                if i == 0:
                    n = misionari
                misionari_right = n - misionari
                canibali_right = n - canibali

                file_string += f"{pozitie_barca[0]} {canibali} canibali {misionari} misionari ...... {pozitie_barca[1]} {canibali_right} canibali {misionari_right} misionari\n"
                if i!=len(output) - 2:
                    if counter_optiuni % 2 == 0:
                        file_string += f"\nBarca s-a deplasat de la malul stang la malul drept cu {canibali - canibali_nou} canibali si {misionari - misionari_nou} misionari\n"
                    elif counter_optiuni % 2 == 1:
                        file_string += f"\nBarca s-a deplasat de la malul drept la malul stang cu {canibali_nou - canibali} canibali si {misionari_nou - misionari} misionari\n"

                
                counter_optiuni += 1

            file.writelines(file_string)




class Graph:
    def __init__(self, startNode, endNodes):
        self.startNode = startNode
        self.endNodes = endNodes

    def scop(self, nodeValue):
        return nodeValue in self.endNodes

    def succesori(self, node):
        lsucc = []
        
        def testConditie(m,c):
            return m==0 or m>=c

        
        if node.value[2] == 1:
            misMalCurent = node.value[0]
            canMalCurent = node.value[1]
            misMalOpus = Graph.N-node.value[0]
            canMalOpus = Graph.N-node.value[1]
        else:
            misMalOpus = node.value[0]
            canMalOpus = node.value[1]
            misMalCurent = Graph.N-node.value[0]
            canMalCurent = Graph.N-node.value[1]
            
        minMisBarca = 0
        maxMisBarca = min(misMalCurent,Graph.M)
        
        for mb in range(minMisBarca,maxMisBarca+1):
            if mb==0:
                minCanBarca = 1
                maxCanBarca = min(canMalCurent,Graph.M)
            else: 
                minCanBarca = 0
                maxCanBarca = min(mb,Graph.M-mb,canMalCurent)
                
                
            for cb in range(minCanBarca,maxCanBarca+1):
                misMalCurentNou = misMalCurent-mb
                canMalCurentNou = canMalCurent-cb
                misMalOpusNou = misMalOpus+mb
                canMalOpusNou = canMalOpus+cb
                
                if not testConditie(misMalCurentNou,canMalCurentNou):
                    continue
                
                if not testConditie(misMalOpusNou,canMalOpusNou):
                    continue
                
                if node.value[2] == 1:
                    valueNodSuccesor = (misMalCurentNou, canMalCurentNou,0)
                else:
                    valueNodSuccesor = (misMalOpusNou, canMalOpusNou, 1)
                    
                    
                if not node.inDrum(valueNodSuccesor):
                    lsucc.append(Node(valueNodSuccesor,node))

        return lsucc



def bfs(graph, nsol=4):
    queue = [Node(graph.startNode)]
    file = open("output.txt", "a")
    file.truncate(0)
    
    while queue:
        curr = queue.pop(0)
        if graph.scop(curr.value):
            # print(repr(curr))
            curr.afisSolFisier(file, repr(curr))
            nsol -= 1
            if nsol == 0:
                return
        succes = graph.succesori(curr)
        queue += succes
      
        
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
                
        


f = open("input.txt","r")
[Graph.N, Graph.M] = f.readline().strip().split()
Graph.N = int(Graph.N)
Graph.M = int(Graph.M)

start = (Graph.N,Graph.N,1)
ends = [(0,0,0)]
gr = Graph(start,ends)
bfs(gr,nsol=3) 



