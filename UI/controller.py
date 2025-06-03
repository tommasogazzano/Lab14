import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choiceNode = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceStore = None

    def fillDD(self):
        stores = self._model.getStores()
        storesDD = map(lambda x : ft.dropdown.Option(text= x.store_id, data = x, on_click = self._readStoreDD), stores)
        self._view._ddStore.options = storesDD
        self._view.update_page()

    def fillNodesDD(self, store_id):
        nodes = self._model.getNodes(store_id)
        nodesDD = map(lambda x: ft.dropdown.Option(text= x.order_id, data= x, on_click= self._readNodeDD), nodes)
        self._view._ddNode.options = nodesDD
        self._view.update_page()

    def _readNodeDD(self, e):
        if e.control.data is None:
            print("errore lettura DD Node")
            self._choiceNode = None
        self._choiceNode = e.control.data
        print(self._choiceNode)

    def _readStoreDD(self, e):
        if e.control.data is None:
            print("errore in lettura DD")
            self._choiceStore = None

        self._choiceStore = e.control.data
        print(self._choiceStore)

    def handleCreaGrafo(self, e):
        store_id = self._view._ddStore.value
        if store_id == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione selezionare uno store dal DD", color = "red"))
            self._view.update_page()
            return

        maxGiorni = self._view._txtIntK.value
        if maxGiorni == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione inserire un valore di Giorni", color = "red"))
            self._view.update_page()
            return

        try:
            intMaxGiorni = int(maxGiorni)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione inserire un valore numerico", color="red"))
            self._view.update_page()
            return

        self._model.build_graph(store_id, intMaxGiorni)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente"))
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"numero Nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"numero Archi: {nEdges}"))
        self._view.update_page()
        self.fillNodesDD(store_id)







    def handleCerca(self, e):
        source = self._view._ddNode.value
        lista = self._model.getBFSNodesFromTree(source)
        for l in lista:
            self._view.txt_result.controls.append(ft.Text(f"{l}"))
        self._view.update_page()

    def handleRicorsione(self, e):
        pass
