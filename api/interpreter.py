# Speichert nur wichtige Daten um schnelle ergebnisse auf einem Json abzuspeichern 
import json


collected_data = {
    "counter": 0,
    "clicks": [],
    "scrollPercentage": 0,
    "scrollMax": 0,
    "scrollData": {},
    "time": [],
    "sectionVisibility": {} 
}


def save_json(data):
    collected_data["clicks"].extend(data["clicks"])    

    # Aktualisieren der Scroll-Daten
    for position, time in data["scrollData"].items():
        if position not in collected_data["scrollData"]:
            collected_data["scrollData"][position] = time
        else:
            collected_data["scrollData"][position] += time

    collected_data["scrollMax"] = data["scrollMax"]

    
    with open('api/collectedData.json', 'w') as json_file:
        json.dump(collected_data, json_file, indent=4)