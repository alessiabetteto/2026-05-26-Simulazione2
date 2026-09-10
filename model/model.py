import copy

import networkx as nx


class Model:
    def __init__(self):
        self._graph = nx.Graph()  # semplice e pesato altrimenti DiGraph()
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
            # se l'hash è una tupla:
            # self._idMapGenes[(g.GeneID, g.Function)] = g


        self._graph.add_nodes_from(self._actors)

        edges = DAO.getAllEdges(rat1, rat2, self._idMapActors)
        for e in edges:
            self._graph.add_edge(e.a1, e.a2, weight=e.peso)

        # quando cerchi all'interno delle liste delle classi e non deve esistere già l'arco
        for a1 in self._allAlbums:
            for a2 in self._allAlbums:
                if a1 != a2:
                    for t1 in a1.tuttiBrani:
                        for t2 in a2.tuttiBrani:
                            if t1 != t2 and t2.GenreId == t1.GenreId and not self._graph.has_edge(a1,
                                                                                                  a2) and not self._graph.has_edge(
                                    a2, a1):
                                self._graph.add_edge(a1, a2)

        # altro metodo per creare gli archi
        for c1 in self._circuiti:
            for c2 in self._circuiti:
                # Confrontando gli ID, valuterai (1, 2) perché 1 < 2,
                # ma non valuterai (2, 1) perché 2 non è minore di 1!
                # Questo elimina sia i doppioni che i nodi con se stessi.
                if c1.circuitId < c2.circuitId:

                    if len(c1.results) > 0 and len(c2.results) > 0:
                        peso_totale = piloti_validi_per_circuito[c1.circuitId] + piloti_validi_per_circuito[
                            c2.circuitId]
                        self._graph.add_edge(c1, c2, weight=peso_totale)


        # altro modo per creare gli archi:
        for i in range(0, len(self._allConstructors)):
            for j in range(i + 1, len(self._allConstructors)):
                nodo1 = self._allConstructors[i]
                nodo2 = self._allConstructors[j]

                # Basterà verificare che entrambi abbiano il dizionario non vuoto
                # (significa che hanno corso nel range)
                if len(nodo1.risultati) > 0 and len(nodo2.risultati) > 0:

                    peso1 = 0
                    for anno1 in nodo1.risultati:
                        for pilota1 in nodo1.risultati[anno1]:
                            # Trasformo in stringa per catturare None, \N e NULL
                            pos1_str = str(pilota1.position).strip().upper()
                            if pos1_str not in ["NULL", "\\N", "NONE", ""]:
                                peso1 += 1

                    peso2 = 0
                    for anno2 in nodo2.risultati:
                        for pilota2 in nodo2.risultati[anno2]:
                            # Stesso controllo per il secondo team
                            pos2_str = str(pilota2.position).strip().upper()
                            if pos2_str not in ["NULL", "\\N", "NONE", ""]:
                                peso2 += 1

                    self._graph.add_edge(nodo1, nodo2, weight=peso1 + peso2)


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

    #oppure se vuoi una lista
    def getTop5ProdottiPiuVenduti(self):

        lista = []

        for u in self._graph.nodes:
            # Chiediamo a networkx di calcolare la somma dei pesi
            peso_uscenti = self._graph.out_degree(u, weight='weight')
            peso_entranti = self._graph.in_degree(u, weight='weight')

            influenza = peso_entranti - peso_uscenti
            lista.append((u, influenza))

        lista_ordinata = sorted(lista, key=lambda x: x[1], reverse=True)[:5]

        return lista_ordinata

    def calcolaRangeEsatto(self, parziale):
        # Converte le stringhe in datetime
        # date_obj = [datetime.strptime(p.dob, '%Y-%m-%d') for p in parziale]
        # se è già un datetime:
        date_obj = [p.dob for p in parziale]

        giovane = max(date_obj)  # Chi è nato "dopo" (max) è il più giovane
        anziano = min(date_obj)  # Chi è nato "prima" (min) è il più anziano

        diff = (giovane - anziano).days  # Differenza in giorni!
        return diff




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



        # ------------------------------------------------------------------------
        # il programma dovrà identificare la componente connessa di dimensione maggiore, e stamparne
        # tutti i nodi, ordinati in senso decrescente di peso minimo degli archi incidenti.

        lista_nodi = []

        # 1. Passo in rassegna tutti i nodi del grafo
        for nodo in subgraph:

            # Prendo tutti gli archi attaccati a questo nodo
            # In un nx.Graph() (non orientato), .edges(nodo) ci dà gli archi incidenti
            archi_incidenti = self._graph.edges(nodo, data=True)

            # Se il nodo è isolato (non ha archi), lo salto (oppure puoi mettergli peso 0)
            if len(archi_incidenti) > 0:

                # 2. Trovo il peso minimo tra tutti questi archi
                # Creo una lista temporanea solo con i pesi di questi archi
                pesi = []
                for u, v, data in archi_incidenti:
                    pesi.append(data['weight'])

                peso_minimo = min(pesi)

                # Salvo nella mia lista finale una tupla (nodo, peso_minimo_trovato)
                lista_nodi.append((nodo, peso_minimo))

        # 3. Ordino la lista in senso decrescente (reverse=True) in base al peso (x[1])
        lista_ordinata = sorted(lista_nodi, key=lambda x: x[1], reverse=True)

        # --------------------------------------------------------------------------



        # ---------------------------------------------------------------------------------------

        # si stampino tutte le componenti connesse del grafo di dim maggiore di 1, in ordine decrescente di dimensione

        # prendere tt componenti connesse
        # La funzione nx.connected_components(self._graph) di NetworkX
        # restituisce una lista di set (insiemi). Ogni set contiene
        # semplicemente i nomi dei nodi che formano quella componente (es. {'G234065', 'G234073'}).

        all_components = list(
            nx.connected_components(self._graph))  # connected_components saranno una lista di nodi connessi tra di loro

        # verificare che la lunghezza sia superiore a 1
        components = [c for c in all_components if len(c) > 1]

        ordinata = sorted(components, key=len, reverse=True)
        return ordinata






        # ----------------------------------------------------------------------------------
        return len(components), largest, details



    # visualizzare artista con grado maggiore, l'artista con somma dei pesi incidenti
    # massima e i 10 archi di peso maggiore, in ordine decrescente di peso (in caso di parità
    # ordinare alfabeticamente per nome del primo artista e poi del secondo

    def stampaInfo(self):

        self._allArtists.sort(key=lambda x: x.name)
        self._final_a = None
        self._grado_max = 0
        for a in self._allArtists:
            if self._graph.degree[a] > self._grado_max:
                self._final_a = a
                self._grado_max = self._graph.degree[a]

        a, somma = None, 0

        for a1 in self._allArtists:
            somma_pesi = 0
            for a2 in self._allArtists:
                if self._graph.has_edge(a1, a2):
                    somma_pesi += self._graph[a1][a2]["weight"]

            if somma_pesi > somma:
                somma = somma_pesi
                a = a1

        # Poiché non possiamo invertire le stringhe (alfabetico) facilmente,
        # togliamo il reverse=True e rendiamo negativo il peso. In questo modo,
        # il numero più grande diventa il più piccolo, ottenendo un ordine decrescente naturale,
        # mentre le stringhe manterranno il loro normale ordine alfabetico crescente.
        # in questo modo ordiniamo in ordine decrescente il peso e crescente i nomi

        archi = sorted(
            self._graph.edges(data=True),
            key=lambda x: (-x[2]['weight'], x[0].name, x[1].name)
        )[:10]

        return self._final_a, self._grado_max, a, somma, archi



    """ estrarre i mesi da un formato 20.05.2025 09:00:00 or smth like that"""
    # Estraiamo i mesi (assicurati che il formato stringa sia corretto o usa un oggetto datetime)
    # Nota: uso split()[0] nel caso ci sia anche l'orario nella stringa del db
    # mese_corr = datetime.strptime(str(nodo_corrente.datetime).split()[0], '%Y-%m-%d').month
    # mese_prec = datetime.strptime(str(nodo_precedente.datetime).split()[0], '%Y-%m-%d').month


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

            # SE NON TI DA IL NODO DI PARTENZA:
            # for nodo in self._graph.nodes:
            #     nodo_partenza = nodo
            #     if nodo.Essential != "?":
            #         essenzialita = nodo.Essential
            #         parziale = [nodo_partenza]
            #         self._ricorsione_path(parziale, essenzialita)
            #
            # return self.best_path, self.best_score

            parziale = [nodo_partenza]

            self._ricorsione_path(parziale)
            return self.best_path, self.best_score

        def _ricorsione_path(self, parziale):

            # # --- 1. CALCOLO COMPONENTI CONNESSE (Regola IV dello spareggio) ---
            # # Creiamo il sottografo con i nodi attuali per contare le componenti
            # subg = self._graph.subgraph(parziale)
            # num_comp = nx.number_connected_components(subg)


            # 1. VALUTAZIONE SOLUZIONE E AGGIORNAMENTO BEST

            # 1.a --> massimizzare la lunghezza
            if len(parziale) > len(self.best_path):
                self.best_path = copy.deepcopy(parziale)  # FONDAMENTALE:  una COPIA !
                self.best_score = len(parziale)  # o calcola la somma dei pesi

            # 1.b --> massimizzare il peso
            peso_corrente = 0
            for i in range(len(parziale) - 1):
                u = parziale[i]
                v = parziale[i + 1]
                peso_corrente += self.grafo[u][v]['weight']

            if peso_corrente > self.best_score:
                self.best_score = peso_corrente
                self.best_path = list(parziale)


            # 2. ESTRAZIONE ULTIMO NODO E RICERCA VICINI

            ultimo_nodo = parziale[-1]

            for vicino in self.grafo.neighbors(ultimo_nodo):  # self._graph.successors se DiGraph() !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if vicino not in parziale:  # Evita di ripassare sugli stessi nodi (niente cicli)

                    # 3. FILTRO DI VALIDITÀ DELLA TRACCIA (DA ADATTARE ALL'ESAME!)
                    is_valid = True  # inizializza sempre a true per sicurezza, e tutti gli altri dovrebberp essere false
                                    # anche se non sono tutti false, almeno nell'ordine true-false
                                    # l'importante è che non ci sia un altro true dopo false!

                    # VARIANTE 1A: Vincolo sull'arco (es. peso crescente)
                    if len(parziale) == 1:
                        is_valid = True  # Il primo arco va sempre bene
                    else:
                        penultimo_nodo = parziale[-2]
                        peso_vecchio = self._graph[penultimo_nodo][ultimo_nodo]['weight']
                        peso_nuovo = self._graph[ultimo_nodo][vicino]['weight']

                        # LO BLOCCO SOLO SE DECRESCE STRETTAMENTE!
                        if peso_nuovo < peso_vecchio:
                            is_valid = False

                    # VARIANTE 1B: Vincolo sul nodo
                    if vicino.Essential == ultimo_nodo.Essential:
                        is_valid = False

                    # 4. BACKTRACKING
                    if is_valid:
                        parziale.append(vicino)
                        self._ricorsione_path(parziale)
                        parziale.pop()  # Torno indietro

        # Massimizzare la Somma di Attributi (Somma dei valori dei NODI)
        def _ricorsione2(self, parziale, peso_accumulato):

            # Valutazione
            if peso_accumulato > self.best_score:
                self.best_score = peso_accumulato
                self.best_path = list(parziale)

            # Esplorazione
            for vicino in self.grafo.neighbors(ultimo):
                if vicino not in parziale:
                    if filtro_valido:
                        peso_arco = self.grafo[ultimo][vicino]['weight']

                        # Passo ricorsivo passando il nuovo peso aggiornato
                        parziale.append(vicino)
                        self._ricorsione(parziale, peso_accumulato + peso_arco)
                        parziale.pop()





    # ABBIAMO UN NODO DI PARTENZA E UNO DI ARRIVO!!!!!
    # variante 1 ma con alcune modifiche
    # la lunghezza sia pari a lun, rispettando i versi, somma pesi archi sia massima

    def cerca_cammino(self, nodo_partenza, nodo_arrivo, lun):
        self.best_path = []
        self.best_score = 0

        parziale = [nodo_partenza]

        # passiamo il peso accumulato come parametro:
        self._ricorsione_path(parziale, nodo_arrivo, lun, 0.0)
        return self.best_path, self.best_score

    def _ricorsione_path(self, parziale, nodo_arrivo, lunghezza_target, peso_corrente):

        # 1. VALUTAZIONE SOLUZIONE E CONDIZIONE DI TERMINAZIONE
        # Controllo se ho raggiunto la lunghezza target (lunghezza_target archi = lunghezza_target + 1 nodi)
        if len(parziale) == lunghezza_target + 1:
            # Controllo se l'ultimo nodo è esattamente quello di arrivo richiesto
            if parziale[-1] == nodo_arrivo:
                # Se il peso è maggiore del best, aggiorno!
                if peso_corrente > self.best_score:
                    self.best_score = peso_corrente
                    self.best_path = list(parziale)
            # Se sono arrivato alla lunghezza massima mi fermo a prescindere
            # (non ha senso continuare a esplorare perché supererei la lunghezza richiesta)
            return

        # 2. ESTRAZIONE ULTIMO NODO E RICERCA VICINI

        ultimo_nodo = parziale[-1]

        for vicino in self._graph.successors(
                ultimo_nodo):  # self._graph.successors se DiGraph() !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if vicino not in parziale:  # Evita di ripassare sugli stessi nodi (niente cicli)

                # 3. FILTRO DI VALIDITÀ DELLA TRACCIA (DA ADATTARE ALL'ESAME!)
                # Calcolo il peso del nuovo arco
                peso_arco = float(self._graph[ultimo_nodo][vicino]['weight'])

                # 4. BACKTRACKING
                parziale.append(vicino)
                self._ricorsione_path(parziale, nodo_arrivo, lunghezza_target, peso_corrente + peso_arco)
                parziale.pop()  # Torno indietro




    """ VARIANTE 2: Quando la traccia chiede di "selezionare un set di N elementi" che NON sono collegati 
    tra loro (es. "nessuno è mai stato compagno di squadra dell'altro", "appartengono a componenti connesse diverse").
    Nota: Questo scheletro estrae prima le componenti e poi lancia la ricorsione su di esse."""

    class Model:
        def __init__(self):
            self.grafo = nx.Graph()
            self.best_set = []
            self.best_valore = 0  # o float('inf') se chiede di minimizzare la differenza di età
            # self._bestMax = None
            # self._best_diff = float('inf')  # Uso una singola variabile per la differenza
            # self._bestMin = None
            # self._bestPath = []


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
                # se è una roba più complessa fai una funzione a parte  es. total_tracks = self._getTotalTracks(parziale) fuori dalla ricorsione
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
                # Calcolo la statistica richiesta (ESEMPIO: somma attributo) che può anche essere una fz a parte
                somma_corrente = sum([n.attributo for n in parziale])
                if somma_corrente > self.best_somma:
                    self.best_somma = somma_corrente
                    self.best_gruppo = copy.deepcopy(parziale)
                return

            # 2. ESPLORAZIONE: Raccolgo i vicini validi di TUTTI i nodi in 'parziale'
            vicini_validi = set()  # Uso il set per non avere doppioni

            for nodo_interno in parziale:
                for vicino in self.grafo.neighbors(nodo_interno):
                    if vicino not in parziale:

                        # 3. FILTRO SULL'ARCO (CORRETTO!)
                        # Controllo che il 'vicino' NON abbia un arco di peso 1
                        # con NESSUNO dei nodi attualmente dentro 'parziale'
                        is_valido = True
                        for nodo_in_parziale in parziale:
                            # Se esiste un arco tra il vicino e un nodo del gruppo...
                            if self._graph.has_edge(vicino, nodo_in_parziale):
                                # ...e quell'arco ha peso 1, scarto il vicino!
                                if self._graph[vicino][nodo_in_parziale]['weight'] == 1:
                                    is_valido = False
                                    break  # Interrompo il ciclo interno, questo vicino è da scartare

                        if is_valido:
                            vicini_validi.add(vicino)

            # 4. BACKTRACKING
            for vicino_scelto in vicini_validi:
                parziale.append(vicino_scelto)
                self._ricorsione_gruppo(parziale, target_N)
                parziale.pop()


    """ cammino depth first!!!!"""

    # Tramite il pulsante “Cerca Percorso Massimo”, si visualizzi il cammino più lungo partendo da un nodo (si
    # scelga l’algoritmo di visita del grafo più opportuno fra visita in ampiezza ed in profondità). Il nodo è
    # selezionato dall’apposito menù a tendina.

    def getCamminoPiuLungo(self, nodo_partenza):
        # Inizializzo la lista che conterrà il percorso migliore trovato
        self._best_cammino = []

        # Faccio partire la ricorsione passandogli il nodo di partenza
        # e un cammino parziale che contiene già il nodo di partenza
        self._ricorsione(nodo_partenza, [nodo_partenza])

        return self._best_cammino

    def _ricorsione(self, nodo_corrente, cammino_parziale):
        # 1. CONDIZIONE DI AGGIORNAMENTO
        # Se il cammino che sto esplorando è più lungo del best che avevo salvato, lo aggiorno.
        if len(cammino_parziale) > len(self._best_cammino):
            self._best_cammino = copy.deepcopy(list(cammino_parziale))  # Faccio una copia della lista!

        # 2. ESPLORAZIONE DEI VICINI (DFS)
        # networkx.DiGraph.successors() ci dà tutti i nodi raggiungibili partendo da nodo_corrente
        for vicino in self._graph.successors(nodo_corrente):

            # Controllo anti-ciclo (buona pratica, anche se qui le date impediscono cicli)
            if vicino not in cammino_parziale:
                # Provo ad aggiungere il vicino al cammino
                cammino_parziale.append(vicino)

                # Faccio ripartire la ricorsione dal vicino
                self._ricorsione(vicino, cammino_parziale)

                # BACKTRACKING: tolgo il vicino per poter esplorare altri rami
                cammino_parziale.pop()


















