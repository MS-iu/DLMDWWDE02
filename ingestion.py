import os
import csv
import psycopg2
import pandas as pd

# Konfigurieren Sie die Verbindung zur PostgreSQL-Datenbank
db_connection = psycopg2.connect(
    dbname="meine-datenbank",
    user="mein-benutzer",
    password="mein-passwort",
    host="datenbank",  # Verweis auf den Datenbank-Container
    port="5432"
)
db_cursor = db_connection.cursor()

# Verzeichnis, in dem die CSV-Dateien gespeichert sind
csv_directory = "/app/csv_data"

# Liste der Dateinamen, die verarbeitet werden sollen
csv_files = os.listdir(csv_directory)

for csv_file in csv_files:
    csv_path = os.path.join(csv_directory, csv_file)

    with open(csv_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Überspringen der Überschriftenzeile

        for row in csv_reader:
            # Annahme: Die CSV-Datei hat Spalten für Datum, Supermarkt, Artikelnummer und Umsatz
            datum, supermarkt, artikelnummer, umsatz = row

            # Fügen Sie die Daten in die PostgreSQL-Datenbank ein
            insert_query = "INSERT INTO meine_tabelle (datum, supermarkt, artikelnummer, umsatz) VALUES (%s, %s, %s, %s)"
            db_cursor.execute(insert_query, (datum, supermarkt, artikelnummer, umsatz))
            db_connection.commit()

# Verbindung zur Datenbank schließen
db_cursor.close()
db_connection.close()
