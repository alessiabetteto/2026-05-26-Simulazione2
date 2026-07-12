import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        ratings = self._model.getRatings()

        for r in ratings:
            self._view._ddrating1.options.append(ft.dropdown.Option(r))
            self._view._ddrating2.options.append(ft.dropdown.Option(r))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        self._graph_creato = False

        if self._view._ddrating1.value is None or self._view._ddrating2.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione! Inserisci un rating", color="red"))
            self._view.update_page()
            return

        if self._view._ddrating1.value < self._view._ddrating2.value:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione! Range non valido.", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(self._view._ddrating1.value, self._view._ddrating2.value)

        Nnodes, Nedges = self._model.getGraphDetails()

        if Nnodes == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(
                    f"Attenzione! Non ci sono attori corrispondenti al range {self._view._ddrating1.value} e {self._view._ddrating2.value}",
                    color="red"))
            self._view.update_page()
            return

        self._graph_creato = True

        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! Il grafo contiene {Nnodes} nodi e {Nedges} archi"))
        self._view.update_page()

        self.handleDettagli(None)
        self.handleInfoConnessa(None)

    def handleDettagli(self, e):

        top5 = self._model.getTop5Archi()

        if top5 == []:
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione! Gli attori non hanno mai lavorato insieme nello stesso film", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Archi di peso maggiore: ", color="red"))

        for a in top5:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} -> {a[1]} (peso: {a[2]["weight"]})"))

        self._view.update_page()

    def handleInfoConnessa(self, e):
        numero, largest, details = self._model.getConnessaInfo()
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {numero} componenti connesse", color="red"))

        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa maggiore ha dimensione pari a {len(largest)}", color="red"))

        for l in largest:
            self._view.txt_result.controls.append(
                ft.Text(l))

        # self._view.txt_result.controls.append(
        #     ft.Text(f"Componente connessa in ordine decrescente di grado dei nodi", color="red"))
        #
        # for d in details:
        #     self._view.txt_result.controls.append(
        #         ft.Text(f"{d[0]} - grado {d[1]}"))

        self._view.update_page()

    def handleCammino(self, e):
        if self._graph_creato == False:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Non ho trovato un grafo su cui calcolare il cammino", color="red"))
            self._view.update_page()
            return

        path = self._model.calcolaPercorso()

        if len(path) == 0:  # non ho trovato un cammino
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Non ho trovato un cammino", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Ecco il cammino migliore:", color="green"))

        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()