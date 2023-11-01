import csv
import random
import datetime
import os

# Anpassbare Parameter
supermarkt_anzahl = 10
tage = 90
artikel_anzahl = 100
kassiererinnen_pro_supermarkt = 3
gesamtziel = 1000000  # Zielanzahl von Datensätzen

# Pfade zum Speichern der CSV-Dateien
volume_csv_directory = '/app/csv_data'
desktop_directory = '/app/csv_data_desktop'
os.makedirs(volume_csv_directory, exist_ok=True)
os.makedirs(desktop_directory, exist_ok=True)

def zufällige_artikelnummer():
    return ["A" + ''.join(random.choice("0123456789") for _ in range(9)) for _ in range(artikel_anzahl)]

def zufällige_uhrzeit():
    return datetime.time(random.randint(8, 19), random.randint(0, 59))

def kassiererinnen_ids():
    return ["ID" + ''.join(random.choice("0123456789") for _ in range(8)) for _ in range(kassiererinnen_pro_supermarkt)]

artikel_liste = zufällige_artikelnummer()
supermärkte = [f"Supermarkt {i + 1}" for i in range(supermarkt_anzahl)]
end_datum = datetime.datetime.now().date()
start_datum = end_datum - datetime.timedelta(days=tage - 1)
datensätze_pro_supermarkt = gesamtziel // supermarkt_anzahl
datensätze_pro_tag = datensätze_pro_supermarkt // tage

for i, supermarkt in enumerate(supermärkte):
    kassiererinnen = kassiererinnen_ids()
    datei_name = f"supermarkt_{i + 1}.csv"

    for j in range(tage):
        aktuelles_datum = start_datum + datetime.timedelta(days=j)
        supermarkt_datensätze = []

        # Jeder Artikel wird mindestens 10-mal hinzugefügt
        for artikel in artikel_liste:
            for _ in range(10):
                umsatz = round(random.uniform(1, 100), 2)
                zeit = zufällige_uhrzeit()
                kassiererin = random.choice(kassiererinnen)
                supermarkt_datensätze.append([aktuelles_datum, zeit, supermarkt, artikel, umsatz, kassiererin])

        # Wenn benötigt, können zusätzliche zufällige Artikel hinzugefügt werden
        while len(supermarkt_datensätze) < datensätze_pro_tag:
            artikel = random.choice(artikel_liste)
            umsatz = round(random.uniform(1, 100), 2)
            zeit = zufällige_uhrzeit()
            kassiererin = random.choice(kassiererinnen)
            supermarkt_datensätze.append([aktuelles_datum, zeit, supermarkt, artikel, umsatz, kassiererin])

        try:
            # Speichern im Volume-Verzeichnis
            with open(os.path.join(volume_csv_directory, datei_name), mode='a', newline='') as datei:
                schreiber = csv.writer(datei)
                if j == 0:
                    schreiber.writerow(["Datum", "Uhrzeit", "Supermarkt", "Artikelnummer", "Umsatz", "Kassiererinnen-ID"])
                for datensatz in supermarkt_datensätze:
                    schreiber.writerow(datensatz)

            # Speichern auf dem Desktop
            with open(os.path.join(desktop_directory, datei_name), mode='a', newline='') as datei:
                schreiber = csv.writer(datei)
                if j == 0:
                    schreiber.writerow(["Datum", "Uhrzeit", "Supermarkt", "Artikelnummer", "Umsatz", "Kassiererinnen-ID"])
                for datensatz in supermarkt_datensätze:
                    schreiber.writerow(datensatz)
        except Exception as e:
            print(f"Fehler beim Schreiben der Datei {datei_name}: {e}")

print(f"{gesamtziel} CSV-Datensätze wurden erstellt.")
