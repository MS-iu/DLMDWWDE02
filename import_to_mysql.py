#!/usr/bin/env python3
# Import data to MySQL
# Dieses Python Skript ist dafür verantwortlich, die generierten Daten in die MySQL-Datenbank zu importieren.
# Dieses Skript hat die längste Laufzeit in der Datenpipline. Versuche mit Big-Data Diensten wie Apache Airflow waren nicht schneller,
# daher wurde dieser Dienst aus Sicht der Wartbarkeit und Zuverlässigkeit beibehalten.


import csv
import mysql.connector


# Verbindung zur MySQL Datenbank herstellen
conn = mysql.connector.connect(
    host='mysql_db',
    user='user',
    password='rootpassword'
)
cursor = conn.cursor()

print("Verbindung zur Datenbank wurde erfolgreich aufgebaut.")


# Datenbank erstellen (falls nicht vorhanden)
cursor.execute("CREATE DATABASE IF NOT EXISTS supermarkt_db")
cursor.execute("USE supermarkt_db")

print("Datenbank wurde erfolgreich erstellt.")

# Definition und Erstellung der Tabelle 'umsatz', wenn sie noch nicht existiert.
# Diese Tabelle speichert den Umsatz pro Artikel, verknüpft mit Datum, Uhrzeit, Supermarkt und Kassiererin
# und ist die Ausgangstabelle für die spätere Aggregation.
cursor.execute("""
CREATE TABLE IF NOT EXISTS umsatz (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Datum DATE,
    Uhrzeit TIME,
    Supermarkt VARCHAR(255),
    Artikelnummer VARCHAR(255),
    Kassiererin_ID VARCHAR(255),
    Umsatz FLOAT
)
""")

print("Tabelle umsatz wurde erfolgreich erstellt.")

# Lese CSV-Dateien aus dem Verzeichnis /app/csv_data und füge die Daten in die Datenbanktabelle ein.
# Die Schleife iteriert durch 10 Supermärkte, entsprechend der Annahme von 10 CSV-Dateien.

path = '/app/csv_data'
for i in range(1, 11):  # Könnte variabel gestaltet werden, ist aktuell fest
    with open(f"{path}/supermarkt_{i}.csv", 'r') as file:
        print(f"{path}/supermarkt_{i}.csv wird geladen.")
        reader = csv.reader(file)
        next(reader)  # Überspringen der Kopfzeile
        for row in reader:
            datum, uhrzeit, supermarkt, artikelnummer, umsatz, kassiererin_id = row
            # Einfügen der Daten in die Tabelle 'umsatz'.
            cursor.execute("INSERT INTO umsatz (Datum, Uhrzeit, Supermarkt, Artikelnummer, Umsatz, Kassiererin_ID) VALUES (%s, %s, %s, %s, %s, %s)",
                           (datum, uhrzeit, supermarkt, artikelnummer, float(umsatz), kassiererin_id))


print("CSV-Dateien wurden erfolgreich geladen.")

# Erstellen einer Tabelle 'import_status' um den Importstatus festzuhalten.
# Erst wenn der Eintrag "completed" in die Tabelle geschrieben ist, startet das Aggregation-Skript.
cursor.execute("""
CREATE TABLE IF NOT EXISTS import_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
# Eintrag des Status 'completed' zeigt den erfolgreichen Abschluss des Importvorgangs.
# Das ist das Startsignal für die Aggregation.
cursor.execute("INSERT INTO import_status (status) VALUES ('completed')")


print("Flagge wurde erfolgreich gesetzt.")


# Speichern der Änderungen in der Datenbank und Schließen der Verbindung.
conn.commit()
cursor.close()
conn.close()

print("Import abgeschlossen.")