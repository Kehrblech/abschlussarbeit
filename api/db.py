import sqlite3
import json

#
# !!! Funktions handle reseved API Data and save with sqlite3 in to collected_data.db
#
def save_data_to_db(data):
    try:
        #1.get all data
        clicks = json.dumps(data.get('clicks', []))
        scroll_percentage = data.get('scrollPercentage', 0)
        scroll_max = data.get('scrollMax', 0)
        scroll_data = json.dumps(data.get('scrollData', {}))
        times = json.dumps(data.get('time', []))
        section_visibility = json.dumps(data.get('sectionVisibility', {}))
        user_agent = json.dumps(data.get('userAgent',{}))
        user_agent_language = json.dumps(data.get('userAgentLanguage',{}))
        url=json.dumps(data.get('url',{})) 
        history_length=json.dumps(data.get('historyLength',0))
        screen_width =  json.dumps(data.get('screenWidth',0))
        screen_height =  json.dumps(data.get('screenHeight',0))
        device =  json.dumps(data.get('device',{}))
        timezone =  json.dumps(data.get('timezone',{}))
        cookies =  json.dumps(data.get('cookies',{}))
        connection_speed =  json.dumps(data.get('connectionSpeed',{}))
        no_tracking =  json.dumps(data.get('noTracking',{}))
        cpu_cores=  json.dumps(data.get('cpuCores',{}))
        referrer=  json.dumps(data.get('referrer',{}))

        #2.use sqlite connect
        conn = sqlite3.connect('collected_data.db')
        cursor = conn.cursor()

        #3.Table erstellen falls noch nicht
        #3.1 //TODO validierungen 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collected_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clicks TEXT,
                scroll_percentage REAL,
                scroll_max REAL,
                scroll_data TEXT,
                times TEXT,
                section_visibility TEXT,
                user_agent TEXT,
                user_agent_language TEXT,
                url TEXT,
                history_length REAL,
                screen_width REAL,
                screen_height REAL,
                device TEXT,
                timezone TEXT,
                cookies TEXT,
                connection_speed TEXT,
                no_tracking TEXT,
                cpu_cores TEXT,
                referrer TEXT
            )
        ''')
        conn.commit()

        #4.Store all data
            
        cursor.execute("INSERT INTO collected_data (clicks, scroll_percentage, scroll_max, scroll_data, times, section_visibility, user_agent, user_agent_language, url, history_length, screen_width, screen_height, device, timezone, cookies, connection_speed, no_tracking, cpu_cores, referrer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (clicks, scroll_percentage, scroll_max, scroll_data, times, section_visibility, user_agent, user_agent_language, url, history_length, screen_width, screen_height, device, timezone, cookies, connection_speed, no_tracking, cpu_cores, referrer))
        conn.commit()

        conn.close()

        return True

    except Exception as e:
        print("!!!ERROR!!!"+str(e))
        return False  
