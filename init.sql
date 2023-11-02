-- Überprüft, ob der Benutzer 'user' existiert, und löscht ihn, falls vorhanden
-- Hilft Konflikte zu vermeiden, wenn der Benutzer bereits existiert
DROP USER IF EXISTS 'user'@'%';
-- Erstellt einen neuen Benutzer 'user' mit der Möglichkeit, sich von jedem Host aus zu verbinden
-- Das Passwort für diesen Benutzer wird auf 'rootpassword' gesetzt
CREATE USER 'user'@'%' IDENTIFIED BY 'rootpassword';
-- Gewährt dem Benutzer 'user' alle Zugriffsrechte auf die Datenbank 'supermarkt_db'
-- Dies umfasst Rechte zum Lesen, Schreiben und Ändern von Daten sowie Verwaltungsaufgaben
GRANT ALL PRIVILEGES ON supermarkt_db.* TO 'user'@'%';
-- Lädt die Zugriffsrechte neu, damit alle Änderungen durch die oben genannten Befehle
-- sofort wirksam werden und der Benutzer die erteilten Rechte nutzen kann
FLUSH PRIVILEGES;
-- Dieses Skript wird in der Datenbank angewendet, um Fehler beim Durchlauf der Pipeline zu vermeiden.
-- Für produktive Systeme müsste eine aus Datenschutz-Sicht optimalere Lösung gefunden werden.