import csv
import random
import datetime
import os

# Anpassbare Parameter
supermarkt_anzahl = 10
datensatz_pro_tag = 1200  # Anzahl der Datensätze pro Tag
tage = 90

# Funktion zur Generierung einer zufälligen 10-stelligen Artikelnummer
def zufällige_artikelnummer():
    artikelnummer = "A" + ''.join(random.choice("0123456789") for _ in range(9))
    return artikelnummer

# Liste von Supermärkten erstellen
supermärkte = [f"Supermarkt {i + 1}" for i in range(supermarkt_anzahl)]

# Anpassung des Zeitraums auf das letzte Quartal (letzte 3 Monate)
end_datum = datetime.datetime(2023, 3, 31)  # Anfang des letzten Monats im Quartal
start_datum = end_datum - datetime.timedelta(days=tage-1)

# CSV-Dateien erstellen
for i, supermarkt in enumerate(supermärkte):
    datei_name = f"supermarkt_{i + 1}.csv"
    supermarkt_datensätze = []

    for _ in range(tage):
        for _ in range(datensatz_pro_tag):
            datum = start_datum + datetime.timedelta(days=tage-1)
            artikelnummer = zufällige_artikelnummer()
            umsatz = round(random.uniform(1, 1000), 2)
            supermarkt_datensätze.append([datum, supermarkt, artikelnummer, umsatz])

    # Pfad zum Volume, in dem die CSV-Dateien gespeichert werden sollen
    volume_csv_directory = '/app/csv_data'

    # Verwende denselben Code zum Erstellen der CSV-Dateien, aber speichere sie im Volume
    with open(os.path.join(volume_csv_directory, datei_name), mode='w', newline='') as datei:
        schreiber = csv.writer(datei)
        schreiber.writerow(["Datum", "Supermarkt", "Artikelnummer", "Umsatz"])
        for datensatz in supermarkt_datensätze:
            schreiber.writerow(datensatz[0:4])

print("CSV-Dateien wurden erstellt.")
