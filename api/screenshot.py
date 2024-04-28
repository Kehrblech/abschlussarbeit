from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import base64
import time
import os
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import undetected_chromedriver as uc

# Hier die Original Quelle zum Screenshot Thema  
# https://www.linkedin.com/pulse/test-automation-how-capture-full-page-screenshots-selenium-nir-tal/
def capture_full_page_screenshot(driver):
    #Senden der CDP-Kommandos, um die Metriken der Seite zu erhalten
    metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    width = metrics['contentSize']['width']
    height = metrics['contentSize']['height']

    # Screenshots auf voller länge
    screenshot = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "clip": {
            "x": 0,
            "y": 0,
            "width": width,
            "height": height,
            "scale": 1
        },
        "captureBeyondViewport": True
    })
    

    return base64.b64decode(screenshot['data'])


# options = Options()
# options.add_argument("--window-size=1920,1080")
# #usign headless mode 
# options.add_argument("--headless")  
# driver = uc.Chrome(options=options)
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")

#manueller pfad für den ChromeDriver // Fix kann auch sein ein Update von Google Chrome zu machen 
chromedriver_path =  'C:/Users/Julian/Downloads/chromedriver-win321/chromedriver-win32/chromedriver.exe'

# WEbdriver definieren mit ChromeDriver-Pfad
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)
# url für den screenshot
driver.get("http://127.0.0.1:5500/heatmap01/index.html")
# driver.get("https://soliq.de") 
time.sleep(1)  


screenshot_data = capture_full_page_screenshot(driver)

# Save as png -> use 
image_name = "Xscreenshot.png"
path = os.getcwd() 
screenshot_path = os.path.join(path, image_name)
with open(screenshot_path, "wb") as file:
    file.write(screenshot_data)

print(f"worked {screenshot_path}")

#TODO!!! Driver quit does not close always  
driver.close()
driver.quit()

