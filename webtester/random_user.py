import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


#path zum 
chromedriver_path = "C:/Users/Julian/Downloads/chromedriver-win32/chromedriver-win32/chromedriver.exe"

#Liste von random User-Agentens Google ergebnisse  
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Mobile Safari/537.36",
]
#TODO Liste von random Languages aber funktioniert nicht muss noch verbessern
languages = [
    "en-US,en;q=0.9",
    "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7"
]

#URL 
url = "http://127.0.0.1:5500/heatmap01/index.html"


def get_random_user_agent():
    return random.choice(user_agents)

def get_random_language():
    return random.choice(languages)

 # random interaktion Perfomen 
def simulate_interaction(driver):
    time.sleep(1)
    # website höhe bekommen 
    max_scroll_height = driver.execute_script("return document.body.scrollHeight")

    # random wohin scrollen 
    random_scroll_position = random.randint(0, max_scroll_height)
    driver.execute_script(f"window.scrollTo(0, {random_scroll_position});")
    print("Scrolled to pos: "+str(random_scroll_position))
    # random wait nach dem Scrollen
    time.sleep(random.uniform(0.5, 1))

    #interaktion Perfomen zwei, a element suchen und clicken
    elements = driver.find_elements(By.TAG_NAME, "a")
    
    if elements:  # check ob die Liste nicht leer ist
        random_element = random.choice(elements)
        pos = random_element.location
        x, y = pos['x'], pos['y']
        if x >= 0 and y >= 0:
            try:
                ActionChains(driver).move_to_element(random_element).perform()
                random_element.click()
                time.sleep(1)
                print("Clicked at: ("+str(x)+","+str(y)+")")
            except Exception as e:
                print(f"Error clicking element: {e}")
        else:
            print("outside")
            
            

# MAIN FUNKTION
def main():
    # Chrome zusammenbasteln Mehr optiopnen hinzufügen 
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # kein window
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(f"accept-language={get_random_language()}")

    # ohne geht nicht!!! WICHTIG  Path ///WENN nicht geht chrome update machen 
    service = Service(executable_path=chromedriver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # aufruf
        driver.get(url)

        # interaktion
        for _ in range(random.randint(1, 2)):  # wie oft anzahl der interaktionen
            simulate_interaction(driver)

    finally:
        # stackoverflow send key action
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER)

        time.sleep(0.5)
        actions.perform()
        time.sleep(1)
        driver.quit()
        print("done")
        
def repeat(number_of_times):
    
    while number_of_times >=0:
        number_of_times -= 1
        main()
        print(str(number_of_times))
        


if __name__ == "__main__":
    repeat(10000)
    



