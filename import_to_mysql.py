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
    Supermarkt VARCHAR(255),
    Artikelnummer VARCHAR(255),
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
            datum, supermarkt, artikelnummer, umsatz = row
            cursor.execute("INSERT INTO umsatz (Datum, Supermarkt, Artikelnummer, Umsatz) VALUES (%s, %s, %s, %s)",
                           (datum, supermarkt, artikelnummer, float(umsatz)))

# Änderungen speichern und Verbindung schließen
conn.commit()
cursor.close()
conn.close()
