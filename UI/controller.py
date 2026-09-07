import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._graph_creato = False


    def fillDDsRating(self):
        ratings = self._model.getRatings()

        for r in ratings:
            self._view._ddrating1.options.append(ft.dropdown.Option(r))
            self._view._ddrating2.options.append(ft.dropdown.Option(r))
        self._view.update_page()

    # che cosa fare quando un dropdown dipende da un altro
    # poi nella view nel dd da cui dipende, ddYear (in questo caso),
    # aggiungi "on_change=self._controller.fillDDShapes"
    # poi subito dopo il solito:  self._controller.fillDDYear()
    def fillDDShapes(self, e):
        year = self._view.ddyear.value

        if year is None:  # <--- Aggiunto controllo di sicurezza
            return

        self._view.ddshape.options.clear()  # <--- Svuota le forme dell'anno precedente

        shapes = self._model.getShapes(year)
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))

        self._view.update_page()


    def fillDDArtista(self):
        artists = sorted(self._model.getAllArtists(), key=lambda a: a.name)
        for a in artists:
            self._view._ddArtista.options.append(ft.dropdown.Option(key=a.id, text=a.name))
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

        if self._view._txtInLun.value == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire lunghezza del cammino", color="red"))
            self._view.update_page()
            return

        try:
            numero_n = int(self._view._txtInN.value)

        except ValueError:
            self._view._txt_result.controls.append(
                ft.Text("Per favore, inserisci un numero intero valido!", color="red")
            )
            self._view.update_page()
            return

        if not self._view._txtIntK:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione! Inserisci prima un valore", color="red"))
            self._view.update_page()
            return

        # RICORDATI DI CONVERTIRE IN INTERI I VALORI CHE PRENDI DALLA VIEW PERCHé ALTRIMENTI
        # LI PRENDI COME "29" xes.
        nodo_partenza = int(self._view._ddProdStart.value)
        nodo_arrivo = int(self._view._ddProdEnd.value)

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



        # SE NON FUNZIONA UN BOTTONE!
        self._view._btnRicorsione.disabled = False
        self._view._ddNode.disabled = False




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

        for i, a in enumerate(archi):
            self._view._txt_result.controls.append(
                ft.Text(f"{i + 1}. {a[0]} -- {a[1]} (peso: {a[2]["weight"]})"))
        self._view.update_page()


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


        # !!!!!!!!!!!!!!!!!!!!!
        album_id_selezionato = int(self._view._ddAlbum.value)

        # 2. Recupero l'oggetto Album vero e proprio dal dizionario del model
        nodo_partenza = self._model._idMapAlbums[album_id_selezionato]

        path, valore = self._model.cerca_sottoinsieme_disconnesso(numero_n, nodo_partenza)

        ordinata = sorted(path, key=lambda x: x.name)



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


        # Se ti servono cosi: A, B, C -> usa il join in questo modo
        lista_nomi = [nodo.GeneID for nodo in c]
        nodi_uniti = ", ".join(lista_nomi)

        self._view.update_page()