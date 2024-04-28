# Bachelorarbeit - Vorhersehbare Benutzerinteraktionen als Alternative zu Drittanbieter-Cookies

## Übersicht

Dieses Repository enthält den Code für mein Bachelorprojekt, das sich auf die Analyse von Benutzerinteraktionen und die Vorhersage von Nutzerverhalten ohne die Verwendung von Drittanbieter-Cookies konzentriert. Das Projekt ist in drei Hauptmodule unterteilt: `api`, `test-website`, und `webtester`.

## Struktur

- **api**: Dieses Verzeichnis enthält den Flask-basierten Server für die Datenerfassung und Analyse, einschließlich der Entscheidungsfindungslogik und des Random Forest Modells zur Vorhersage von Benutzeraktionen.
- **test-website**: Hier befindet sich der Code für die Website, die zur Erfassung von Benutzerengagement-Daten verwendet wird. 
- **webtester**: Dieses Modul enthält Skripte für die Auswertung der Cookie-Daten und einen Zufallsgenerator für Nutzerinteraktionen, der im Rahmen des Testens der Hypothesen der Arbeit eingesetzt wird.

## Modulfunktionen

- `api`:
  - Flask API zur Handhabung von Anfragen
  - Analyseoberfläche und zugehörige Python Module für die Visualisierung von Daten   
  - SQLite3 Datenverarbeitung
  - Entscheidungslogik 
  - Random Forest Analyse
- `auswertungen_cookies`:
  - Auswertungen und Ergebnisse der Cookie Analysen
- `test-website`:
  - HTML und CSS Frontend für die Datenerfassung von Benutzerinteraktionen
  - Java Script für die Datenerfassung
- `webtester`:
  - Tools zur Auswertung von Cookie-Daten
  - Simulator für zufällige Benutzerinteraktionen

## Nutzung

Jedes Modul kann unabhängig voneinander gestartet werden, je nach den Anforderungen der Tests oder der Analyse. Es ist wichtig, dass die `api` immer läuft, wenn die `test-website` oder der `webtester` verwendet werden, da diese auf die API zur Datenübermittlung angewiesen sind.
