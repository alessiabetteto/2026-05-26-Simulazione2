from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct (avg_rating )
                        from ratings r
                        order by avg_rating asc"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])


        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(rat1, rat2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT n.* FROM names n, role_mapping rm, ratings r
                    WHERE n.id = rm.name_id 
                    AND rm.movie_id = r.movie_id 
                    AND r.avg_rating BETWEEN %s AND %s
                    AND n.date_of_birth IS NOT NULL"""

        cursor.execute(query, (rat1, rat2))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(rat1, rat2, idMapActor):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.id as a1, n1.id as a2, SUM( cast((REPLACE(m.worlwide_gross_income, '$ ', '')) AS DECIMAL ) ) AS peso 
                        from role_mapping rm ,role_mapping rm1,  ratings r, names n, names n1, movie m
                        where rm.movie_id = rm1.movie_id  
                        and rm.name_id < rm1.name_id 
                        and rm.movie_id = r.movie_id 
                        and rm.name_id = n.id 
                        and rm1.name_id = n1.id  
                        and rm.movie_id = m.id 
                        and rm1.movie_id = m.id
                        and r.avg_rating between  %s and %s
                        AND m.worlwide_gross_income IS NOT NULL
                        and n.date_of_birth is not null  and n1.date_of_birth is not null 
                        group by n.id, n.name, n.height, n.date_of_birth, n.known_for_movies,
                            n1.id, n1.name, n1.height, n1.date_of_birth, n1.known_for_movies 
                        order by peso desc"""

        cursor.execute(query, (rat1, rat2))

        for row in cursor:
            results.append(Arco(idMapActor[row["a1"]], idMapActor[row["a2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

    """ a. L'utente seleziona dal corrispondente menù a tendina un genere 
    cinematografico (tabella genre) e inserisce un intero $K$ in un TextField.
    b. Premendo il pulsante "Crea grafo", l'applicazione costruisce un grafo NON orientato e pesato. 
    I vertici sono tutti i film che appartengono al genere selezionato e che hanno almeno una valutazione 
    nella tabella ratings.
    c. Esiste un arco tra due film distinti se e solo se i due film hanno in comune almeno $K$ attori 
    (usando la tabella role_mapping con categoria 'actor' o 'actress').
    d. Il peso dell'arco è pari al numero esatto di attori che i due film hanno in comune."""

    # query corrispondente:
    # select v1.id, v2.id2, count(*) as peso
    # from (select distinct (m.id ) as id, rm.name_id  as n1
    # from movie m, ratings r , role_mapping rm , genre g
    # where m.id = r.movie_id and rm.movie_id = m.id
    # and m.id = g.movie_id and g.genre = "Drama"
    # and rm.category = "actress") as v1,
    # ( select distinct (m.id ) as id2, rm.name_id  as n2
    # from movie m, ratings r , role_mapping rm , genre g
    # where m.id = r.movie_id and rm.movie_id = m.id
    # and m.id = g.movie_id and g.genre = "Drama"
    # and rm.category = "actress") as v2
    # where v1.id < v2.id2 and v1.n1 = v2.n2
    # group by v1.id, v2.id2
    # having count(*) >= 2
    # order by peso desc



    """ Testo del Punto 1:

        a. L'utente seleziona da un menù a tendina un anno di uscita (tabella movie).
        
        b. Premendo il pulsante "Crea grafo", l'applicazione costruisce un grafo NON orientato e pesato. 
        I vertici sono tutti i registi (tabella names unita a director_mapping) che hanno diretto almeno un film nell'anno selezionato dall'utente.
        
        c. Esiste un arco tra due registi se nel corso della loro intera carriera (non solo nell'anno selezionato) 
        hanno diretto film appartenenti ad almeno un genere in comune.
        
        d. Il peso dell'arco è il numero di generi distinti che i due registi hanno in comune."""




