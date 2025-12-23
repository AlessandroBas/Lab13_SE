from database.DB_connect import DBConnect
from model.gene import Gene

class DAO:

    @staticmethod
    def read_cromosomi():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        query = """ SELECT DISTINCT cromosoma
                    FROM gene
                    WHERE cromosoma <> 0"""

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row['cromosoma'])
        except Exception as e:
            print(f"Errore durante la query read_cromosomi: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def read_geni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        query = """ SELECT *
                    FROM gene """

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(query)
            for row in cursor:
                result.append(Gene(**row))
        except Exception as e:
            print(f"Errore durante la query read_geni: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def read_connesioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        query = """ SELECT g1.id AS gene1, g2.id AS gene2, i.correlazione
                FROM gene g1, gene g2, interazione i 
                WHERE  g1.id = i.id_gene1 and g2.id = i.id_gene2 
                       and g2.cromosoma != g1.cromosoma
                       and g2.cromosoma>0
                       and g1.cromosoma>0
                GROUP BY g1.id, g2.id, i.correlazione"""

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(query)
            for row in cursor:
                result.append((row['gene1'], row['gene2'], row['correlazione']))

        except Exception as e:
            print(f"Errore durante la query read_connessioni: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result