import mysql.connector
import os
import json
import random

def ir(connection, db):
    try:
        if connection.is_connected():
            print("Connessione al database riuscita")

            # Seleziona il database
            connection.database = db
            alfa = connection.cursor()
            alfa.execute("USE STORAGE")
            # Esegui una query per selezionare tutte le righe dalla tabella
            query = "SELECT * FROM KPIS;"
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)

            # Recupera tutte le righe
            rows = cursor.fetchall()

            # Restituisci le righe in formato JSON
            return json.dumps(rows)

    except mysql.connector.Error as err:
        print(f"Errore di connessione al database: {err}")

def show_databases(connection):
    try:
        if connection.is_connected():
            print("Connessione al database riuscita")

            # Esegui il comando SHOW DATABASES;
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES;")

            # Visualizza i risultati
            print("Elenco dei database:")
            for (db,) in cursor:
                print(db)

    except mysql.connector.Error as err:
        print(f"Errore durante l'esecuzione della query: {err}")
        
        
        
def add_kpis(connection, n):
    try:
        if connection.is_connected():
            print("Connessione al database riuscita")

            # Seleziona il database
            connection.database = "STORAGE"

            # Prepara e esegui le query di inserimento
            cursor = connection.cursor()

            for i in range(1, n+1):
                name = f"KPI_{i}"
                value = random.uniform(1.0, 100.0)

                query = f"INSERT INTO KPIS (NOME, VALORE) VALUES ('{name}', {value});"
                cursor.execute(query)

            # Conferma le modifiche
            connection.commit()
            print(f"Inserite {n} righe nella tabella KPIS")

    except mysql.connector.Error as err:
        print(f"Errore di connessione al database: {err}")

# Connessione al database
connection = None
database = os.environ.get("MYSQL_DATABASE")
user = "root"
password = "smartapp"
host = os.environ.get("targetip", "127.0.0.1")
port = os.environ.get("port", 3306)

try:
    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connection established")
        
        
#        add_kpis(connection, 100)
    

        # Chiamata alla funzione show_databases
        show_databases(connection)

        # Chiama la funzione ir e stampa il risultato
        result = ir(connection, "STORAGE")
        print(result)

except mysql.connector.Error as err:
    print(f"Errore di connessione al database: {err}")

finally:
    # Chiudi la connessione
    if connection and connection.is_connected():
        connection.close()
        print("Connessione al database chiusa")

