import csv
import random

# Erstellen Sie eine Liste von Supermarktdaten
supermarkt_daten = []
for i in range(10):  # Beispiel: 10 Zeilen Daten
    supermarkt_name = f"Supermarkt {i + 1}"
    anzahl_kunden = random.randint(100, 1000)
    umsatz = round(random.uniform(1000, 10000), 2)

    daten = [supermarkt_name, anzahl_kunden, umsatz]
    supermarkt_daten.append(daten)

# Speichern Sie die Daten in der vorhandenen CSV-Datei und überschreiben Sie sie
csv_datei = "supermarkt_daten.csv"
with open(csv_datei, mode='w', newline='') as datei:
    schreiber = csv.writer(datei)
    schreiber.writerow(["Supermarkt", "Anzahl Kunden", "Umsatz"])
    schreiber.writerows(supermarkt_daten)

print("CSV-Datei wurde aktualisiert: supermarkt_daten.csv")