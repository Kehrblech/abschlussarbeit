import sqlite3
import json

def aggregate_and_save_to_json(database_path, output_json_path):
    #Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    #Daten aus der Datenbank abrufen
    cursor.execute('SELECT * FROM collected_data')
    rows = cursor.fetchall()

    #Datenbankstruktur in ein leeres  Datenobjekt übertragen
    col_avg_data = {
        "counter": 0,
        "clicks": [],
        "scrollPercentage": 0,
        "scrollMax": 0,
        "scrollData": {},
        "time": [],
        "sectionVisibility": {}
    }

    #Durchschnitt berechnen
    total_records = len(rows)
    for row in rows:
        clicks = json.loads(row[0])
        col_avg_data["counter"] += 1
        col_avg_data["clicks"].extend(clicks)

        col_avg_data["scrollMax"] += row[2]

        col_avg_data["scrollPercentage"] += row[1]

        scroll_data = json.loads(row[3])
        for position, time in scroll_data.items():
            if position not in col_avg_data["scrollData"]:
                col_avg_data["scrollData"][position] = time
            else:
                col_avg_data["scrollData"][position] += time

    #durchschnittswerte berechnen
    if total_records > 0:
        col_avg_data["scrollPercentage"] /= total_records
        for position in col_avg_data["scrollData"]:
            col_avg_data["scrollData"][position] /= total_records

    #als json speichern 
    with open(output_json_path, 'w') as json_file:
        json.dump(col_avg_data, json_file, indent=4)

    #close db 
    conn.close()

#Beispielaufruf der Funktion
aggregate_and_save_to_json('collected_data.db', 'aggregated_data.json')
