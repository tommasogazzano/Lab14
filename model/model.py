import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap = {}
        self._ordini = []
        self._grafo = nx.DiGraph()


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