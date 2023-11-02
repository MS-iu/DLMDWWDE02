# Supermarkt Data Generator
# Dieses Python Skript ist zuständig für das Erzeugen der fiktiven Supermarktdaten.

import csv
import random
import datetime
import os

# Die Parameter wurden nach Erstellung des Skripts nicht durchgängig variabel in anderen Skripten verwendet.
# Von einer Änderung wird daher abgeraten.

supermarkt_anzahl = 10  # Anzahl der Supermärkte
tage = 90   # Anzahl der Tage, für die Daten generiert werden
artikel_anzahl = 100    # Anzahl unterschiedlicher Artikel
kassiererinnen_pro_supermarkt = 3   # Anzahl der Kassiererinnen pro Supermarkt
gesamtziel = 1200000  # Zielanzahl von Datensätzen

# Pfade zum Speichern der CSV-Dateien
# Hier ist keine Anpassung mehr notwendig.
# Im Docker-compose File muss der Pfad für die Speicherung der Daten auf der lokalen Maschine aber unbedingt angepasst werden.
volume_csv_directory = '/app/csv_data'
desktop_directory = '/app/csv_data_desktop'
os.makedirs(volume_csv_directory, exist_ok=True)
os.makedirs(desktop_directory, exist_ok=True)

def zufällige_artikelnummer():
    # Generiert eine Liste zufälliger Artikelnummern
    return ["A" + ''.join(random.choice("0123456789") for _ in range(9)) for _ in range(artikel_anzahl)]

def zufällige_uhrzeit():
    # Erzeugt eine zufällige Uhrzeit für die Transaktionen
    return datetime.time(random.randint(8, 19), random.randint(0, 59))

def kassiererinnen_ids():
    # Generiert eine Liste zufälliger IDs für Kassiererinnen
    return ["ID" + ''.join(random.choice("0123456789") for _ in range(8)) for _ in range(kassiererinnen_pro_supermarkt)]

artikel_liste = zufällige_artikelnummer()
supermärkte = [f"Supermarkt {i + 1}" for i in range(supermarkt_anzahl)]
end_datum = datetime.datetime.now().date()
start_datum = end_datum - datetime.timedelta(days=tage - 1)
datensätze_pro_supermarkt = gesamtziel // supermarkt_anzahl # Verteilung der Datensätze auf Supermärkte
datensätze_pro_tag = datensätze_pro_supermarkt // tage  # Datensätze pro Tag und Supermarkt

for i, supermarkt in enumerate(supermärkte):
    kassiererinnen = kassiererinnen_ids()
    datei_name = f"supermarkt_{i + 1}.csv"

    for j in range(tage):
        aktuelles_datum = start_datum + datetime.timedelta(days=j)
        supermarkt_datensätze = []

        # Generiere Datensätze für jeden Artikel, wobei jeder mindestens 20-mal hinzugefügt wird
        for artikel in artikel_liste:
            for _ in range(20):
                umsatz = round(random.uniform(1, 500), 2) # zufälliger Umsatz
                zeit = zufällige_uhrzeit()  # zufällige Uhrzeit
                kassiererin = random.choice(kassiererinnen) # zufällig gewählte Kassiererin
                supermarkt_datensätze.append([aktuelles_datum, zeit, supermarkt, artikel, umsatz, kassiererin])

        # Ergänze zufällige Datensätze, bis die tägliche Zielanzahl erreicht ist
        while len(supermarkt_datensätze) < datensätze_pro_tag:
            artikel = random.choice(artikel_liste)
            umsatz = round(random.uniform(1, 100), 2)
            zeit = zufällige_uhrzeit()
            kassiererin = random.choice(kassiererinnen)
            supermarkt_datensätze.append([aktuelles_datum, zeit, supermarkt, artikel, umsatz, kassiererin])

        try:
            # CSV-Daten im Volume-Verzeichnis speichern
            with open(os.path.join(volume_csv_directory, datei_name), mode='a', newline='') as datei:
                schreiber = csv.writer(datei)
                if j == 0:  # Schreibe Kopfzeilen nur am ersten Tag
                    schreiber.writerow(["Datum", "Uhrzeit", "Supermarkt", "Artikelnummer", "Umsatz", "Kassiererinnen-ID"])
                for datensatz in supermarkt_datensätze:
                    schreiber.writerow(datensatz)

            # CSV-Daten auf dem angegebenen Pfad speichern
            with open(os.path.join(desktop_directory, datei_name), mode='a', newline='') as datei:
                schreiber = csv.writer(datei)
                if j == 0:  # Schreibe Kopfzeilen nur am ersten Tag
                    schreiber.writerow(["Datum", "Uhrzeit", "Supermarkt", "Artikelnummer", "Umsatz", "Kassiererinnen-ID"])
                for datensatz in supermarkt_datensätze:
                    schreiber.writerow(datensatz)
        except Exception as e:
            print(f"Fehler beim Schreiben der Datei {datei_name}: {e}")

print(f"{gesamtziel} CSV-Datensätze wurden erstellt.")  # Abschlussmeldung nach der Generierung
