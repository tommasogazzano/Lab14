import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap = {}
        self._ordini = []
        self._grafo = nx.DiGraph()
        self._bestPath = []
        self._maxCost = 0


    def build_graph(self, store_id, maxGiorni):
        self._grafo.clear()
        self.getNodes(int(store_id))
        if len(self._ordini) == 0:
            print("Attenzione, lista vuota!!")
            return

        self._grafo.add_nodes_from(self._ordini)
        self.addEdges(int(store_id), maxGiorni)



    def printGraphDetails(self):
        print(f"Grafo correttamente creato, con {len(self._grafo.nodes())} nodi e {len(self._grafo.edges())} archi")


    def getStores(self):
        return DAO.DAOgetStores()

    def getNodes(self, store_id):
        self._ordini = DAO.DAOgetNodes(store_id)
        for ordine in self._ordini:
            self._idMap[ordine.order_id] = ordine
        return self._ordini

    def addEdges(self, store_id, maxGiorni):
        allEdges = DAO.DAOgetEdges(store_id, maxGiorni, self._idMap)
        for e in allEdges:
            if e.o1 in self._grafo and e.o2 in self._grafo:
                self._grafo.add_edge(e.o1, e.o2, weight = e.peso)

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, self._idMap[int(source)])
        nodi = list(tree.nodes())
        return nodi[1:]

    def getBestPath(self, startStr):
        self._bestPath = []
        self._maxCost = 0

        start = self._idMap[int(startStr)]

        parziale = [start]

        vicini = self._grafo.neighbors(start)
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestScore
    

    def _ricorsione(self, parziale):
        if self.getScore(parziale) > self._maxCost:
            self._bestScore = self.getScore(parziale)
            self._bestPath = copy.deepcopy(parziale)

        for v in self._grafo.neighbors(parziale[-1]):
            if (v not in parziale and #check if not in parziale
                    self._grafo[parziale[-2]][parziale[-1]]["weight"] >
                    self._grafo[parziale[-1]][v]["weight"]): #check if peso nuovo arco è minore del precedente
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def getScore(self, listOfNodes):
        tot = 0
        for i in range(len(listOfNodes) - 1):
            tot += self._grafo[listOfNodes[i]][listOfNodes[i + 1]]["weight"]

        return tot