import sqlite3
import matplotlib.pyplot as plt
import io
import base64
import json
from datetime import datetime
import matplotlib.dates as mdates
from collections import Counter
from user_agents import parse


#´Betriebssysteme analysieren
def get_user_agent_count():
    conn = sqlite3.connect('collected_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_agent FROM collected_data')
    user_agents = cursor.fetchall()
    os_counts = {}  # Dynamisches Dictionary für Betriebssysteme
    for ua in user_agents:
        user_agent = parse(ua[0])
        os_family = user_agent.os.family
        if os_family in os_counts:
            os_counts[os_family] += 1
        else:
            os_counts[os_family] = 1
    conn.close()
    print('Verteilung der Betriebssysteme:', os_counts)
    return os_counts

#zahl der clicks ermitteln
def get_click_count():
    conn = sqlite3.connect('collected_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT clicks FROM collected_data')
    clicks = cursor.fetchall()
    total_clicks = sum(len(json.loads(click[0])) for click in clicks)
    conn.close()
    return total_clicks

#Durchschnittliche Aufenthaltszeit berechnen
def get_average_time():
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('collected_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT times FROM collected_data')
    times = cursor.fetchall()
    total_time = 0
    for entry in times:
        time_data = json.loads(entry[0])
        if time_data:
            total_time += sum([t['leave'] - t['entry'] for t in time_data])
    average_time = total_time / len(times) if times else 0
    conn.close()
    return average_time

#Clicks pro stunde für balkendiagramm
def get_data_from_db():
    conn = sqlite3.connect('collected_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT clicks FROM collected_data")
    rows = cursor.fetchall()
    all_clicks = [json.loads(row[0]) for row in rows if row[0]]
    # get h count cliocks per sec.
    click_hours = []
    for clicks in all_clicks:
        for click in clicks:
            click_time = datetime.utcfromtimestamp(click['time'] / 1000.0)
            click_hours.append(click_time.hour)  # only sec

    clicks_per_hour = Counter(click_hours)
    conn.close()
    return clicks_per_hour
    
#balkendiagramm aus den clicks pro stunde
def create_chart(clicks_per_hour):
   
    hours = sorted(clicks_per_hour.keys())
    clicks = [clicks_per_hour[hour] for hour in hours]

    plt.figure(figsize=(10, 6))
    
    
    plt.bar(hours, clicks, color='#6638B6')

    plt.title('Klicks nach Stunden')
    plt.xlabel('Stunde des Tages')
    plt.ylabel('Anzahl der Klicks')
    plt.xticks(hours, [f'{hour}:00' for hour in hours]) 

    img = io.BytesIO()
    plt.savefig(img, format='png',transparent=True)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url
#scroll% data bekommen 
def get_scroll_data_from_db():
    conn = sqlite3.connect('collected_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT scroll_percentage FROM collected_data")
    rows = cursor.fetchall()
    
    scroll_percentage_values = [row[0] for row in rows if row[0] is not None]
    conn.close()
    return scroll_percentage_values

#scroll_percentage_values in histogram
def create_scroll_histogram(scroll_percentage_values):
    plt.figure(figsize=(10, 6))
    
    # Histogram
    plt.hist(scroll_percentage_values, bins=20, color='#6638B6', edgecolor='black')
    
    plt.title('Verteilung des Maximalen Scrollens')
    plt.xlabel('Maximales Scrollen in Prozent der Seitenlänge')
    plt.ylabel('Anzahl der Benutzer')

    img = io.BytesIO()
    plt.savefig(img, format='png',transparent=True)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    return plot_url

def create_stay_time_pie_chart():
    try:
        conn = sqlite3.connect('collected_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT times FROM collected_data")
        rows = cursor.fetchall()

        total_time_on_page_list = []

        for row in rows:
            data = json.loads(row[0])
            if data: 
                if 'entry' in data[0] and 'leave' in data[0]:
                    entry_time = data[0]['entry']
                    leave_time = data[0]['leave']
                    #ToDo milisekunden umrechnen 
                    total_time_on_page = (leave_time - entry_time) / 1000  
                    total_time_on_page_list.append(total_time_on_page)

        conn.close()

        if not total_time_on_page_list:
            return None 

        # Dursch. in Miun und Sek 
        average_stay_time_seconds = sum(total_time_on_page_list) / len(total_time_on_page_list)
        average_stay_time_minutes = int(average_stay_time_seconds // 60)
        average_stay_time_seconds = int(average_stay_time_seconds % 60)

        # Max Min staytime
        max_stay_time_seconds = max(total_time_on_page_list)
        max_stay_time_minutes = int(max_stay_time_seconds // 60)
        max_stay_time_seconds = int(max_stay_time_seconds % 60)

        min_stay_time_seconds = min(total_time_on_page_list)
        min_stay_time_minutes = int(min_stay_time_seconds // 60)
        min_stay_time_seconds = int(min_stay_time_seconds % 60)

        # Kuchendiagramm
        plt.figure(figsize=(10, 6))
        labels = [
            f'Durchschnitt: {average_stay_time_minutes} min {average_stay_time_seconds} s',
            f'Längste: {max_stay_time_minutes} min {max_stay_time_seconds} s',
            f'Kürzeste: {min_stay_time_minutes} min {min_stay_time_seconds} s'
        ]
        times = [average_stay_time_seconds, max_stay_time_seconds, min_stay_time_seconds]
        colors = ['#6638B6', '#FF5733', '#FFD700']

        plt.pie(times, labels=labels, autopct='%1.1f%%', colors=colors,
                textprops={'fontsize': 14})  

        plt.title('Aufenthaltsdauer', fontsize=16)  
        plt.axis('equal')  

        # ToDo Rotate achsen beschrif
        plt.xticks(rotation=45)
        plt.yticks(rotation=45)


        img = io.BytesIO()
        plt.savefig(img, format='png',transparent=True)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()
        return plot_url

    except Exception as e:
        print("!!!ERROR!!! " + str(e))
        return None
    
    
conn = sqlite3.connect('collected_data.db')
cursor = conn.cursor()

#Durchschnittliche scrollgeschwindigkeit berechnen
def calculate_average_scroll_speed():
    cursor.execute("SELECT AVG(scroll_percentage) FROM collected_data")
    average_scroll_speed = cursor.fetchone()[0]
    return average_scroll_speed

#häufigkeit von clicks pro Zeiteinheit berechnen
def calculate_click_frequency():
    cursor.execute("SELECT COUNT(*) FROM collected_data")
    click_frequency = cursor.fetchone()[0]
    return click_frequency

def get_db_connection():
    conn = sqlite3.connect('collected_data.db')
    conn.row_factory = sqlite3.Row  # Optional: Ermöglicht den Zugriff auf die Daten als Dictionaries
    return conn

def get_popular_sections():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT section_visibility FROM collected_data")
        sections_data = cursor.fetchall()
        section_counts = {}

        for data in sections_data:
            section_visibility = json.loads(data[0])
            for section, milliseconds in section_visibility.items():
                duration_in_minutes = milliseconds / 60000  # Umrechnung von Millisekunden in Minuten
                if section in section_counts:
                    section_counts[section] += duration_in_minutes
                else:
                    section_counts[section] = duration_in_minutes

        popular_sections = sorted(section_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        return popular_sections
    finally:
        conn.close() # Stelle sicher, dass die Verbindung am Ende der Anfrage geschlossen wird

#Durchschnittliche CPU-Nutzung berechnen was schwasinn ist aber wer kann der kann, sag ich immer. 
def calculate_average_cpu_usage():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT AVG(cpu_cores) FROM collected_data")
        average_cpu_usage = cursor.fetchone()[0]
        return average_cpu_usage
    finally:
        conn.close()


def get_most_used_resolution():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT screen_width, screen_height FROM collected_data")
        resolutions_data = cursor.fetchall()
        resolution_counts = {}
        for resolution in resolutions_data:
            resolution_str = f"{resolution[0]}x{resolution[1]}"
            if resolution_str in resolution_counts:
                resolution_counts[resolution_str] += 1
            else:
                resolution_counts[resolution_str] = 1
        most_used_resolution = max(resolution_counts, key=resolution_counts.get)
        return most_used_resolution
    finally:
        conn.close()

def get_most_used_language():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_agent_language FROM collected_data")
        languages_data = cursor.fetchall()
        language_counts = {}
        for language in languages_data:
            if language[0] in language_counts:
                language_counts[language[0]] += 1
            else:
                language_counts[language[0]] = 1
        most_used_language = max(language_counts, key=language_counts.get)
        return most_used_language
    finally:
        conn.close()
        
def calculate_average_max_scroll():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT AVG(scroll_percentage) FROM collected_data")
        average_max_scroll = cursor.fetchone()[0]
        return int(average_max_scroll)
    finally:
        conn.close()
        

def get_most_popular_browsers():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_agent FROM collected_data")
        user_agents = cursor.fetchall()
        browser_counts = {}

        for ua in user_agents:
            browser = parse(ua[0]).browser.family  # Extrahiert den Browsernamen aus dem user_agent String
            if browser in browser_counts:
                browser_counts[browser] += 1
            else:
                browser_counts[browser] = 1

        # Sortieren der Browser nach ihrer Häufigkeit und Auswählen der Top-Browser
        most_popular_browsers = sorted(browser_counts.items(), key=lambda x: x[1], reverse=True)
        return most_popular_browsers
    finally:
        conn.close()

# Scrollgeschwindigkeiten
# def create_scroll_histogram():
#     cursor.execute("SELECT scroll_percentage FROM collected_data")
#     scroll_percentages = [row[0] for row in cursor.fetchall()]
#     plt.figure(figsize=(10, 6))
#     plt.hist(scroll_percentages, bins=20, color='#6638B6', edgecolor='black')
#     plt.title('Verteilung des Maximalen Scrollens')
#     plt.xlabel('Maximales Scrollen in Prozent der Seitenlänge')
#     plt.ylabel('Anzahl der Benutzer')
#     img = io.BytesIO()
#     plt.savefig(img, format='png', transparent=True)
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
#     plt.close()
#     return plot_url

# Funktionen aufrufen und Metriken berechnen
average_scroll_speed = calculate_average_scroll_speed()
click_frequency = calculate_click_frequency()
popular_sections = get_popular_sections()
average_cpu_usage = calculate_average_cpu_usage()
most_used_resolution = get_most_used_resolution()
most_used_language = get_most_used_language()
# scroll_histogram_url = create_scroll_histogram()

# Verbindung zur Datenbank schließen nicht schon wieder vergessen 
conn.close()