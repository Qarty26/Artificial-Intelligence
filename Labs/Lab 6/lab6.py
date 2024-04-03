import copy

class NodArbore:
    # g = cost, h = euristica
    def __init__(self, info, g=0, h=0, parent=None):
        self.info = info
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def drumRadacina(self):
        nod = self
        list = [nod]
        while nod.parent is not None:
            nod = nod.parent
            list.append(nod)
        return list[::-1]

    def inDrum(self, infonod):
        nod = self
        while nod is not None:
            if nod.info == infonod:
                return True
            nod = nod.parent
        return False

    def __eq__(self, other):
        return self.g == other.g and self.f == other.f

    def __lt__(self, other):
        return self.f < other.f or (self.f == other.f and self.g > other.g)

    def __str__(self):
        return f"({str(self.info)}, g:{self.g}, f:{self.f})"

    def __repr__(self):
        return "{} ({})".format(str(self.info), "->".join([str(x) for x in self.drumRadacina()]))

    def __hash__(self):
        return hash(self.info)


class Graph:
    def __init__(self, start, scopes):
        self.start = start
        self.scopes = scopes

    def valideaza(self):
        matrDesfasurata = self.start[0] + self.start[1] + self.start[2]
        countInversions = 0
        for i in range(len(matrDesfasurata)):
            for j in range(i + 1, len(matrDesfasurata)):
                if matrDesfasurata[i] > matrDesfasurata[j] and matrDesfasurata[i] and matrDesfasurata[j]:
                    countInversions += 1

        return countInversions % 2 == 0

    def scop(self, infoNode):
        return infoNode == self.scopes

    def estimeaza_h(self, infoNode):
        if self.scop(infoNode):
            return 0

        minH =  float('inf')
        h = 0
        for iLinie, linie in enumerate(self.scopes):
            for iPlacuta, placuta in enumerate(linie):
                if infoNode[iLinie][iPlacuta] != placuta:
                    h += 1

        if h < minH:
            minH = h

        return minH

    def successors(self, node):
        successorsList = []
        foundEmpty = False
        for lGol in range(3):
            for cGol in range(3):
                if node.info[lGol][cGol] == 0:
                        foundEmpty = True
                        break
            if foundEmpty:
                break

        directions = [[-1,0], [1, 0], [0, 1], [0, -1]]
        for d in directions:
            lPlacuta = lGol + d[0]
            cPlacuta = cGol + d[1]
            if lPlacuta < 0 or lPlacuta > 2 or cPlacuta < 0 or cPlacuta > 2:
                continue
            infoSuccessor = copy.deepcopy(node.info)
            infoSuccessor[lGol][cGol], infoSuccessor[lPlacuta][cPlacuta] = infoSuccessor[lPlacuta][cPlacuta], infoSuccessor[lGol][cGol]
            if not node.inDrum(infoSuccessor):
                successorsList.append(NodArbore(infoSuccessor, node.g + 1, self.estimeaza_h(infoSuccessor), node))
        return successorsList



def aStarSolMultiple(graph, nsol=1):
    c = [NodArbore(graph.start)]
    while len(c) > 0:
        node = c.pop(0)
        if graph.scop(node.info):
            print(repr(node))
            nsol -= 1
            if nsol == 0:
                return
        successors = graph.successors(node)
        if successors is not None:
            c.extend(successors)
            c.sort()


def aStar(gr):
    if not gr.valideaza():
        print("No solutions!")
        return
    OPEN = [NodArbore(gr.start)]
    CLOSED = []
    while OPEN:
        nodCurent = OPEN.pop(0)
        CLOSED.append(nodCurent)
        if gr.scop(nodCurent.info):
            print(repr(nodCurent))
            return
        lSuccesori = gr.successors(nodCurent)
        for s in lSuccesori:
            gasitOpen = False
            for nodC in OPEN:
                if s.info == nodC.info:
                    gasitOpen = True
                    if s < nodC:
                        OPEN.remove(nodC)
                    else:
                        lSuccesori.remove(s)
                    break
            if not gasitOpen:
                for nodC in CLOSED:
                    if s.info == nodC.info:
                        if s < nodC:
                            CLOSED.remove(nodC)
                        else:
                            lSuccesori.remove(s)
                        break
        OPEN += lSuccesori
        OPEN.sort()
    print("No solutions here!")


f = open("input5.txt", "r")
continut = f.read()
start = [list(map(int,linie.strip().split())) for linie in continut.strip().split('\n')]  
scopuri = [[1,2,3],
           [4,5,6],
           [7,8,0]       
]



gr = Graph(start,scopuri)
aStar(gr)