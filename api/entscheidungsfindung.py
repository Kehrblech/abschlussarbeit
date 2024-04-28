import json
import sqlite3

#einfahce get longest section 
def get_longest_section_visited(section_visibility_json):
    try:
        sections = json.loads(section_visibility_json)
    except json.JSONDecodeError:
        return None

    longest_section = None
    max_duration = -1
    for section, duration in sections.items():
        if duration > max_duration:
            max_duration = duration
            longest_section = section
    
    return longest_section

def get_stay_time(time):
    try:
        times_data = json.loads(time)
        #Berechne die verweildauer für den ersten (und in diesem fall einzigen) eintrag
        if times_data:  #uberprüfe ob die list inträge enthält
            first_entry = times_data[0]
            entry_time = first_entry['entry']
            leave_time = first_entry['leave']
            #ms 
            duration_ms = leave_time - entry_time
            
            #ms in sec
            stay_time = duration_ms / 1000
            
            
        else:
            stay_time = 0
    except json.JSONDecodeError:
        stay_time = 0
    return stay_time
#sql to db
conn = sqlite3.connect('collected_data.db')
cursor = conn.cursor()

# Get alle benötigten daten für Entscheidungsfindungsmodell
cursor.execute("""
    SELECT id, section_visibility, clicks, scroll_percentage, times FROM collected_data;
""")
rows = cursor.fetchall()

for row in rows:
    anonym_id, section_visibility, clicks, scroll_percentage, times = row
    
    #get längst besuchteste section 
    longest_section_visited = get_longest_section_visited(section_visibility)

    #bestimme Click anzahl 
    try:
        clicks_count = len(json.loads(clicks))
    except json.JSONDecodeError:
        clicks_count = 0
        
    stay_duration = get_stay_time(times)
    
    
    #Fuzzy logic als proof of concept
    # if clicks_count > 5:
    #     next_action = 'clicks_item'
    # elif scroll_percentage > 50 and longest_section_visited and stay_duration > 120:  # Angenommen, >120 Sekunden gilt als lang
    #     next_action = f"stays_in_section_{longest_section_visited}_long"
    # elif scroll_percentage > 50 and longest_section_visited and stay_duration <= 120:  # <=120 Sekunden könnte als kurz bis mittel betrachtet werden
    #     next_action = f"stays_in_section_{longest_section_visited}_short"
    # elif scroll_percentage < 10 and clicks_count == 0 and stay_duration < 30:  # Angenommen, <30 Sekunden gilt als sehr kurz
    #     next_action = 'leaves_page_quickly'
    # elif scroll_percentage < 10 and clicks_count == 0:  # Längere Verweildauer aber wenig Interaktion
    #     next_action = 'leaves_page'
    if clicks_count > 5:  # Wenn mehr als 5 Klicks dann wird angenommen das der Nutzer etwas anklickt
        next_action = 'clicks_item'
    elif scroll_percentage > 50 and longest_section_visited:  # Wenn die Scroll-Tiefe größer als 50% und eine Sektion am längsten besucht wurde
        next_action = f"stays_in_section_{longest_section_visited}"
    elif scroll_percentage < 10 and clicks_count == 0:  #  Wenn kaum gescrollt und nicht geklickt wurde vielleicht hat der Nutzer die Seite verlassen
        next_action = 'leaves_page'
    else:  # keine  bedingungen erfüllt wird
        next_action = 'unknown'
        
    # update für datensatz next_action festlegen
    cursor.execute("""
        UPDATE collected_data
        SET next_action = ?
        WHERE id = ?;
    """, (next_action, anonym_id))


conn.commit()
conn.close()
