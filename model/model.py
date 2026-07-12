class Model:
    def __init__(self):
        self._graph = nx.Graph()  # semplice e pesato
        self._actors = []
        self._idMapActors = {}
        self._bestPath = []

    # lab 12 simulazione per slz a questo problema

    def getRatings(self):
        return DAO.getAllRatings()

    def buildGraph(self, rat1, rat2):
        self._graph.clear()
        self._actors = DAO.getAllNodes(rat1, rat2)

        for a in self._actors:
            self._idMapActors[a.id] = a

        self._graph.add_nodes_from(self._actors)

        edges = DAO.getAllEdges(rat1, rat2, self._idMapActors)
        for e in edges:
            self._graph.add_edge(e.a1, e.a2, weight=e.peso)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)



        # Costruito il grafo, l’applicazione visualizza il numero di vertici e archi e l’artista con maggiore influenza.
        # L’influenza di un artista è calcolata come: peso archi uscenti − peso archi entranti. Inoltre, si visualizzino i 5
        # archi con peso maggiore, in ordine decrescente.

    def getArtistaPiuInfluente(self):
        self._bestArtista = None
        self._maxInfluenza = -1000

        for u in self._graph.nodes:
            # Chiediamo a networkx di calcolare la somma dei pesi
            peso_uscenti = self._graph.out_degree(u, weight='weight')
            peso_entranti = self._graph.in_degree(u, weight='weight')

            influenza_attuale = peso_uscenti - peso_entranti

            # Se troviamo un record migliore, aggiorniamo
            if influenza_attuale > self._maxInfluenza:
                self._bestArtista = u
                self._maxInfluenza = influenza_attuale

        return self._bestArtista, self._maxInfluenza




    def getTop5Archi(self):
        return sorted(self._graph.edges(data=True), key= lambda x: x[2]['weight'], reverse=True)[:5]

    def getConnessaInfo(self):
        # prendere tt componenti connesse
        components = list(nx.connected_components(self._graph))  # connected_components saranno una lista di nodi connessi tra di loro

        # identificare la componente connessa di dimensione maggiore, e stamparne tutti i nodi, ordinati in senso
        # decrescente secondo il grado dei nodi.

        largest = max(components, key=len)

        subgraph = self._graph.subgraph(largest).copy()  # qual è il sottografo costituito dalla componente maggiore

        orderedNodes = sorted(subgraph.nodes(), key=lambda n: self._graph.degree(n), reverse=True)  # ordiniamo secondo il grado dei nodi1

        # mi faccio una lista di tuple in cui il primo elemento è il nodo e il secondo il grado
        details = [(n, self._graph.degree(n)) for n in orderedNodes]

        return len(components), largest, details









    """ estrarre solo l'anno dalla date_published in movie """

    # su SQL:

    # -- Estrae solo l 'anno dal film --
    # SELECT STRFTIME('%Y', date_published) as anno
    # FROM movie
    # -- Se ti chiede i film usciti ad Agosto: --
    # SELECT * FROM movie
    # WHERE STRFTIME('%m', date_published) = '08'

    # oppure in python:
    # from datetime import datetime
    # data_obj = datetime.strptime(row['date_published'], '%Y-%m-%d')
    # anno = data_obj.year

    """ scegliere solo una delle lingue nella lista """

    # SQL:

    # -- Trova tutti i film in cui tra le lingue c'è il francese --
    # SELECT * FROM movie WHERE languages LIKE '%French%'

    #python:
    # lingua_scelta = "French"
    # if lingua_scelta in movie.languages:

    """ calcolare età attore al momento dell'uscita del film """

    # SELECT
    #     CAST(STRFTIME('%Y', m.date_published) AS INTEGER) -
    #     CAST(STRFTIME('%Y', n.date_of_birth) AS INTEGER) AS eta_sul_set
    # FROM movie m, names n, role_mapping r
    # WHERE m.id = r.movie_id AND n.id = r.name_id

    """ la fz coalesce che trasforma i null in 0"""

    # SELECT title, COALESCE(worldwide_gross_income, 0) as incasso
    # FROM movie

    """ se all'utente chiede di inserire una data ed è nel formato datepicker, devi gestirlo cosi: """

    # nel model:
    # def handle_crea_grafo(self, e):
    #     # 1. Recupero il valore dal DatePicker (è un oggetto datetime o None)
    #     data_scelta = self.view.date_picker.value
    #
    #     # 2. Controllo il None!
    #     if data_scelta is None:
    #         self.view.create_alert("Attenzione: devi prima selezionare una data!")
    #         return
    #
    #     # 3. Se arrivo qui, data_scelta è un oggetto datetime.
    #     # Lo passo al model.
    #     self.model.crea_grafo(data_scelta)

    # nel DAO:
    # def get_nodi_by_data(data_obj):
    #     # Formatto l'oggetto datetime nella stringa "YYYY-MM-DD"
    #     # %Y = anno a 4 cifre, %m = mese a 2 cifre, %d = giorno a 2 cifre
    #     data_stringa = data_obj.strftime("%Y-%m-%d")
    #
    #     query = """
    #     SELECT * FROM movie
    #     WHERE date_published = ?
    #     """
    #
    #     # Ora passo la stringa pulita alla query!
    #     cursor.execute(query, (data_stringa,))
    #     return cursor.fetchall()


    """ known for movies: contiene uno o più film. Se il testo ti chiede "Trova tutti gli 
    attori che sono famosi per il film con id 12345", devi scrivere la query così: """
    # SELECT name
    # FROM names
    # WHERE known_for_movies LIKE '%12345%';

    # su python :
    # # Supponiamo che il dato dal db sia la stringa "12345, 67890"
    # campo_db = "12345, 67890"
    #
    # if campo_db is not None:
    #     # Divido la stringa usando la virgola come separatore
    #     lista_id_film = campo_db.split(",")
    #
    #     # Ora ho una vera lista Python: ['12345', ' 67890']
    #     numero_film_famosi = len(lista_id_film)


    """  RICORDA CHE NAMES CONTIENE SIA ATTORI PURI, SIA REGISTI PURI, CHE ATTORI - REGISTI
    Dammi tutti gli attori che hanno ANCHE diretto un film  """
    # SELECT DISTINCT n.name
    # FROM names n, director_mapping dm, role_mapping rm
    # WHERE n.id = dm.name_id   -- Condizione 1: il suo ID compare tra i registi
    # AND n.id = rm.name_id   -- Condizione 2: il suo ID compare ANCHE tra gli attori

    """ avg rating vs mediana"""
    # 1. L'Average Rating (avg_rating - La Media Aritmetica)
    # È la classica media che tutti conosciamo. Prendi la somma di tutti i voti ricevuti dal film e la dividi per il numero totale di votanti (total_votes).
    #
    # Il problema della media: È molto sensibile ai "valori anomali" (outliers) o ai troll (review bombing).
    #
    # Esempio: Se 9 persone danno un voto di 10 a un film, ma un hater (per abbassare la media) dà un voto di 1, la media matematica scende a 9.1. Quel singolo voto estremo ha trascinato giù il risultato.
    #
    # 2. Il Median Rating (median_rating - La Mediana)
    # La mediana è il "valore centrale". Immagina di prendere tutti i voti dati dagli utenti, dal più basso al più alto, e metterli in fila indiana. La mediana è esattamente il voto che sta a metà della fila.
    #
    # Il vantaggio della mediana: Ignora completamente i voti estremi e ti dà un'idea molto più realistica di cosa pensa la "maggioranza" vera del pubblico.
    #
    # Esempio di prima: Voti ordinati: [1, 10, 10, 10, 10, 10, 10, 10, 10, 10]. Il valore che sta fisicamente in mezzo a questa lista è 10. La mediana non si è fatta fregare dall'hater!






    # PUNTO 2 !!!!!!!!!!!!!!!!!!!!!!!!!!!


    """ VARIANTE 1: Quando usarlo: Quando la traccia chiede di "trovare il percorso/cammino"
     di lunghezza o peso massimo a partire da un nodo, rispettando una regola di monotònia
      (es. peso sempre crescente, età decrescente)."""

    import networkx as nx

    class Model:
        def __init__(self):
            self.grafo = nx.Graph()  # o DiGraph
            self.best_path = []
            self.best_score = 0.0  # Usa 0 per pesi/lunghezze, usa float('inf') se devi minimizzare

        def cerca_cammino(self, nodo_partenza):
            self.best_path = []
            self.best_score = 0.0

            parziale = [nodo_partenza]

            self._ricorsione_path(parziale)
            return self.best_path, self.best_score

        def _ricorsione_path(self, parziale):
            # 1. VALUTAZIONE SOLUZIONE E AGGIORNAMENTO BEST
            # ESEMPIO: Cerco la lunghezza massima (cambia con la somma dei pesi se richiesto)
            if len(parziale) > len(self.best_path):
                self.best_path = list(parziale)  # FONDAMENTALE: fai una COPIA con list()!
                self.best_score = len(parziale)  # o calcola la somma dei pesi

            # 2. ESTRAZIONE ULTIMO NODO E RICERCA VICINI
            ultimo_nodo = parziale[-1]

            for vicino in self.grafo.neighbors(ultimo_nodo):
                if vicino not in parziale:  # Evita di ripassare sugli stessi nodi (niente cicli)

                    # 3. FILTRO DI VALIDITÀ DELLA TRACCIA (DA ADATTARE ALL'ESAME!)
                    is_valid = False

                    # VARIANTE 1A: Vincolo sull'arco (es. peso decrescente)
                    if len(parziale) == 1:
                        is_valid = True  # Il primo arco va sempre bene
                    else:
                        penultimo_nodo = parziale[-2]
                        peso_vecchio = self.grafo[penultimo_nodo][ultimo_nodo]['weight']
                        peso_nuovo = self.grafo[ultimo_nodo][vicino]['weight']
                        if peso_nuovo < peso_vecchio:  # Regola: strettamente decrescente
                            is_valid = True

                    # VARIANTE 1B: Vincolo sul nodo (es. età decrescente)
                    # if vicino.eta < ultimo_nodo.eta:
                    #     is_valid = True

                    # 4. BACKTRACKING
                    if is_valid:
                        parziale.append(vicino)
                        self._ricorsione_path(parziale)
                        parziale.pop()  # Torno indietro


    """ VARIANTE 2: Quando usarlo: Quando la traccia chiede di "selezionare un set di N elementi" che NON sono collegati 
    tra loro (es. "nessuno è mai stato compagno di squadra dell'altro", "appartengono a componenti connesse diverse").
    Nota: Questo scheletro estrae prima le componenti e poi lancia la ricorsione su di esse."""

    class Model:
        def __init__(self):
            self.grafo = nx.Graph()
            self.best_set = []
            self.best_valore = 0  # o float('inf') se chiede di minimizzare la differenza di età

        def cerca_sottoinsieme_disconnesso(self, target_N, nodo_partenza=None):
            self.best_set = []
            self.best_valore = 0

            # 1. ESTRAGGO LE COMPONENTI CONNESSE (lista di liste di nodi)
            componenti_connesse = [list(c) for c in nx.connected_components(self.grafo)]

            parziale = []
            componenti_rimanenti = componenti_connesse.copy()

            # Se la traccia obbliga a partire da un nodo specifico:
            if nodo_partenza:
                parziale.append(nodo_partenza)
                # Rimuovo la componente del nodo di partenza per non pescarci più
                componenti_rimanenti = [c for c in componenti_connesse if nodo_partenza not in c]

            self._ricorsione_subset(parziale, componenti_rimanenti, target_N)
            return self.best_set

        def _ricorsione_subset(self, parziale, comp_rimanenti, target_N):
            # 1. CONDIZIONE DI TERMINAZIONE
            if len(parziale) == target_N:
                # Calcolo il punteggio di questa combinazione (DA ADATTARE!)
                # ESEMPIO: Somma dei brani
                punteggio_corrente = sum([nodo.num_brani for nodo in parziale])

                if punteggio_corrente > self.best_valore:
                    self.best_valore = punteggio_corrente
                    self.best_set = list(parziale)
                return

            # 2. CONDIZIONE DI STOP (non ho abbastanza componenti per arrivare a target_N)
            if len(comp_rimanenti) == 0 or len(parziale) + len(comp_rimanenti) < target_N:
                return

            # 3. ESPLORAZIONE: Prendo la prima componente disponibile
            componente_corrente = comp_rimanenti[0]

            # PROVO AD AGGIUNGERE UN NODO QUALSIASI DI QUESTA COMPONENTE
            for nodo in componente_corrente:
                parziale.append(nodo)
                # Chiamo la ricorsione togliendo la componente appena usata (comp_rimanenti[1:])
                self._ricorsione_subset(parziale, comp_rimanenti[1:], target_N)
                parziale.pop()  # Backtracking

            # 4. (Opzionale) DECIDO DI NON USARE NESSUN NODO DI QUESTA COMPONENTE
            # e passo alla prossima. Spesso necessario per trovare l'ottimo globale!
            self._ricorsione_subset(parziale, comp_rimanenti[1:], target_N)


    """ VARIANTE 3: Quando usarlo: Quando la traccia non chiede un "cammino" lineare, 
    ma un "gruppo" (set) di N nodi in cui ogni nuovo nodo aggiunto basta che sia collegato ad 
    almeno uno dei nodi già presenti nel gruppo. Di solito c'è un vincolo sugli archi vietati (es. "peso != 1")."""

    class Model:
        def __init__(self):
            self.grafo = nx.Graph()
            self.best_gruppo = []
            self.best_somma = 0

        def cerca_gruppo_connesso(self, nodo_partenza, target_N):
            self.best_gruppo = []
            self.best_somma = 0

            parziale = [nodo_partenza]

            self._ricorsione_gruppo(parziale, target_N)
            return self.best_gruppo

        def _ricorsione_gruppo(self, parziale, target_N):
            # 1. CONDIZIONE DI TERMINAZIONE ESATTA
            if len(parziale) == target_N:
                # Calcolo la statistica richiesta (ESEMPIO: somma attributo)
                somma_corrente = sum([n.attributo for n in parziale])
                if somma_corrente > self.best_somma:
                    self.best_somma = somma_corrente
                    self.best_gruppo = list(parziale)
                return

            # 2. ESPLORAZIONE: Raccolgo i vicini validi di TUTTI i nodi in 'parziale'
            vicini_validi = set()  # Uso il set per non avere doppioni

            for nodo_interno in parziale:
                for vicino in self.grafo.neighbors(nodo_interno):
                    if vicino not in parziale:

                        # 3. FILTRO SULL'ARCO (DA ADATTARE!)
                        # ESEMPIO: Non posso usare archi di peso = 1
                        peso_arco = self.grafo[nodo_interno][vicino]['weight']
                        if peso_arco != 1:
                            vicini_validi.add(vicino)

            # 4. BACKTRACKING
            for vicino_scelto in vicini_validi:
                parziale.append(vicino_scelto)
                self._ricorsione_gruppo(parziale, target_N)
                parziale.pop()


















