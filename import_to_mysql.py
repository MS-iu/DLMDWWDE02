#!/usr/bin/env python3

import csv
import mysql.connector

# Verbindung zur MySQL Datenbank herstellen
conn = mysql.connector.connect(
    host='mysql_db',
    user='user',
    password='rootpassword'
)
cursor = conn.cursor()

# Datenbank erstellen (falls nicht vorhanden)
cursor.execute("CREATE DATABASE IF NOT EXISTS supermarkt_db")
cursor.execute("USE supermarkt_db")

# Tabelle erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS umsatz (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Datum DATE,
    Uhrzeit TIME,
    Supermarkt VARCHAR(255),
    Artikelnummer VARCHAR(255),
    Kassiererin_ID VARCHAR(255),  # Korrektur hier
    Umsatz FLOAT
)
""")

# CSV-Dateien einlesen
path = '/app/csv_data'
for i in range(1, 11):  # 10 Supermärkte
    with open(f"{path}/supermarkt_{i}.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Überspringen Sie die Kopfzeile
        for row in reader:
            datum, uhrzeit, supermarkt, artikelnummer, umsatz, kassiererin_id = row
            cursor.execute("INSERT INTO umsatz (Datum, Uhrzeit, Supermarkt, Artikelnummer, Umsatz, Kassiererin_ID) VALUES (%s, %s, %s, %s, %s, %s)",
                           (datum, uhrzeit, supermarkt, artikelnummer, float(umsatz), kassiererin_id))

print("CSV-Dateien wurden erfolgreich geladen.")

cursor.execute("""
CREATE TABLE IF NOT EXISTS import_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("INSERT INTO import_status (status) VALUES ('completed')")


print("Flagge wurde erfolgreich gesetzt.")


# Änderungen speichern und Verbindung schließen
conn.commit()
cursor.close()
conn.close()

print("Import abgeschlossen.")