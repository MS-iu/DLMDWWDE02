import csv
import random
import datetime
import os

# Anpassbare Parameter
supermarkt_anzahl = 10
datensatz_pro_tag = 1200  # Maximaler Umsatz pro Tag
tage = 90
artikel_anzahl = 500  # Anzahl der Artikel, die generiert werden sollen

# Pfad zum Volume, in dem die CSV-Dateien gespeichert werden sollen
volume_csv_directory = '/app/csv_data'
os.makedirs(volume_csv_directory, exist_ok=True)


def zufällige_artikelnummer():
    return ["A" + ''.join(random.choice("0123456789") for _ in range(9)) for _ in range(artikel_anzahl)]


artikel_liste = zufällige_artikelnummer()

supermärkte = [f"Supermarkt {i + 1}" for i in range(supermarkt_anzahl)]
end_datum = datetime.datetime.now().date()
start_datum = end_datum - datetime.timedelta(days=tage - 1)

for i, supermarkt in enumerate(supermärkte):
    datei_name = f"supermarkt_{i + 1}.csv"
    supermarkt_datensätze = []

    for j in range(tage):
        aktuelles_datum = start_datum + datetime.timedelta(days=j)

        # Generiere für jeden Artikel an diesem Tag einen Umsatz
        for artikel in artikel_liste:
            umsatz = round(random.uniform(1, datensatz_pro_tag), 2)
            supermarkt_datensätze.append([aktuelles_datum, supermarkt, artikel, umsatz])

    with open(os.path.join(volume_csv_directory, datei_name), mode='w', newline='') as datei:
        schreiber = csv.writer(datei)
        schreiber.writerow(["Datum", "Supermarkt", "Artikelnummer", "Umsatz"])
        for datensatz in supermarkt_datensätze:
            schreiber.writerow(datensatz)

print("CSV-Dateien wurden erstellt.")
