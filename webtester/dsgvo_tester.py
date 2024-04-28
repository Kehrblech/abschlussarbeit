from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse, parse_qs
import tldextract
import time
import re




urls = [
    'https://www.google.com/',
    'https://www.youtube.com/',
    'https://www.facebook.com/',
    'https://www.baidu.com/',
    'https://www.wikipedia.org/',
    'https://www.twitter.com/',
    'https://www.instagram.com/',
    'https://www.linkedin.com/',
    'https://www.pinterest.com/',
    'https://www.reddit.com/',
    'https://www.ebay.com/',
    'https://www.netflix.com/',
    'https://www.amazon.com/',
    'https://www.craigslist.org/',
    'https://www.microsoft.com/',
    'https://www.imgur.com/',
    'https://www.tumblr.com/',
    'https://www.apple.com/',
    'https://www.paypal.com/',
    'https://www.github.com/',
    'https://www.google.co/',
    'https://www.yahoo.com/',
    'https://www.live.com/',
    'https://www.flickr.com/',
    'https://www.dailymotion.com/',
    'https://www.wikia.com/',
    'https://www.blogger.com/',
    'https://www.alibaba.com/',
    'https://www.vimeo.com/',
    'https://www.dropbox.com/',
    'https://www.soundcloud.com/',
    'https://www.spotify.com/',
    'https://www.booking.com/',
    'https://www.microsoftonline.com/',
    'https://www.etsy.com/',
    'https://www.zillow.com/',
    'https://www.quora.com/',
    'https://www.tripadvisor.com/',
    'https://www.salesforce.com/',
    'https://www.adobe.com/',
    'https://www.trello.com/',
    'https://www.shopify.com/',
    'https://www.medium.com/',
    'https://www.skype.com/',
    'https://www.slack.com/',
    'https://www.wix.com/',
    'https://www.weebly.com/',
    'https://www.squarespace.com/',
    'https://www.jimdo.com/',
    'https://www.wordpress.com/',
    'https://www.godaddy.com/',
    'https://www.bluehost.com/',
    'https://www.hostgator.com/',
    'https://www.namecheap.com/',
    'https://www.siteground.com/',
    'https://www.w3schools.com/',
    'https://www.stackoverflow.com/',
    'https://www.github.io/',
    'https://www.bitbucket.org/',
    'https://www.digitalocean.com/',
    'https://www.heroku.com/',
    'https://www.aws.amazon.com/',
    'https://www.google.cloud/',
    'https://www.azure.microsoft.com/',
    'https://www.cloudflare.com/',
    'https://www.mailchimp.com/',
    'https://www.constantcontact.com/',
    'https://www.sendinblue.com/',
    'https://www.getresponse.com/',
    'https://www.hubspot.com/',
    'https://www.marketo.com/',
    'https://www.salesloft.com/',
    'https://www.pipedrive.com/',
    'https://www.zendesk.com/',
    'https://www.freshdesk.com/',
    'https://www.intercom.com/',
    'https://www.drift.com/',
    'https://www.hootsuite.com/',
    'https://www.buffer.com/',
    'https://www.sproutsocial.com/',
    'https://www.canva.com/',
    'https://www.adobe.spark.com/',
    'https://www.picmonkey.com/',
    'https://www.figma.com/',
    'https://www.sketch.com/',
    'https://www.invisionapp.com/',
    'https://www.proto.io/',
    'https://www.axure.com/',
    'https://www.uxpin.com/',
    'https://www.mockplus.com/',
    'https://www.miro.com/',
    'https://www.airtable.com/',
    'https://www.smartsheet.com/',
    'https://www.asana.com/',
    'https://www.monday.com/',
    'https://www.clickup.com/',
    'https://www.basecamp.com/',
]

urls = [
    'https://www.artizon.museum/'
]





persistent_count_all = 0
session_count_all = 0
different_domain_count_all = 0
secure_count_all = 0
http_only_count_all = 0
same_site_none_count_all = 0
third_party_blocked_count_all = 0 




def count_thirdparty_cookie_warnings(logs, main_domain):
    global third_party_blocked_count_all
    third_party_blocked_count = 0
    third_party_urls = set()

    for entry in logs:
        message = entry.get('message', '')
        if "cookie" in message.lower() and "blocked" in message.lower():
            third_party_blocked_count += 1
            third_party_blocked_count_all += 1
        if re.findall(r'https?://[^\s]+', message):
            urls2=re.findall(r'https?://[^\s]+', message)
            for url in urls2:
                if main_domain not in url:
                    third_party_urls.add(url)
        extracted_urls = extract_urls_from_csp(logs,main_domain)
    return third_party_blocked_count, third_party_urls, extracted_urls

def extract_urls_from_csp(logs,main_domain):
    extracted_urls = []
    for log in logs:
        if "Content Security Policy directive" in log['message']:
            urls = re.findall(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]+(?:\/[^\s]*)?", log['message'])
            extracted_urls.append(urls)
    
    return extracted_urls

def cookie_analysis(cookies, extracted_domain):
    global persistent_count_all
    global session_count_all
    global different_domain_count_all
    global http_only_count_all
    global secure_count_all
    global same_site_none_count_all
    persistent_count = 0
    session_count = 0
    different_domain_count = 0
    secure_count = 0
    http_only_count = 0
    same_site_none_count = 0

    for cookie in cookies:
        if 'expiry' in cookie:
            persistent_count += 1
            persistent_count_all += 1
        else:
            session_count += 1
            session_count_all += 1

        if extracted_domain not in cookie['domain']:
            different_domain_count += 1
            different_domain_count_all += 1

        if cookie.get('secure'):
            secure_count += 1
            session_count_all += 1

        if cookie.get('httpOnly'):
            http_only_count += 1
            http_only_count_all += 1

        if cookie.get('sameSite') == 'None':
            same_site_none_count += 1
            same_site_none_count_all += 1
    return {
        'persistent_count': persistent_count,
        'session_count': session_count,
        'different_domain_count': different_domain_count,
        'secure_count': secure_count,
        'http_only_count': http_only_count,
        'same_site_none_count': same_site_none_count
    }

def old_browser_logging():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    for url in urls:
        try:
            driver.get(url)
            parsed_url = urlparse(url)
            current_domain = parsed_url.netloc
            extracted_domain = tldextract.extract(current_domain)
            extracted_domain = "{}.{}".format(extracted_domain.domain, extracted_domain.suffix)
            #interaktionen simul
            actions = ActionChains(driver)
            actions.move_to_element(wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))).perform()
            time.sleep(1)  

            cookies = driver.get_cookies()
            
            for cookie in cookies:
                print(f"{cookie}")
            analysis_results = cookie_analysis(cookies, extracted_domain)

            logs = driver.get_log('browser')
            # for log in logs: 
            #     print(log)
            third_party_cookie_warnings, third_party_cookie_url, extracted_urls= count_thirdparty_cookie_warnings(logs,extracted_domain)

            print(f"URL: {url}")
            print(f"Domain: {extracted_domain}")
            print("Cookie-Analyse-Ergebnisse:")
            for key, value in analysis_results.items():
                print(f"{key}: {value}")
            print(f"Third-Party Blocked: {third_party_cookie_warnings}")
            print(f"Extern URL's: {third_party_cookie_url}")
            print(f"Violations: {len(extracted_urls)}")
            print(f"Violaitions: {extracted_urls}")
        except Exception as e: 
            print(f'Fehler beim Zugriff auf {url}: {e}')

    driver.quit()


def browser_logging():
    #WICHTIG aufbau des frames  COLOUMN weise! 
    results_df = pd.DataFrame(columns=['URL', 'Domain', 'Persistent_Cookies', 'Session_Cookies', 'Different_Domain_Cookies', 'Secure_Cookies', 'HttpOnly_Cookies', 'SameSite_None_Cookies', 'Third_Party_Blocked', 'External_URLs', 'CSP_Violations'])

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    for url in urls:
        try:
            driver.get(url)
            parsed_url = urlparse(url)
            current_domain = parsed_url.netloc
            extracted_domain = tldextract.extract(current_domain)
            extracted_domain = "{}.{}".format(extracted_domain.domain, extracted_domain.suffix)

            actions = ActionChains(driver)
            actions.move_to_element(wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))).perform()
            time.sleep(1)  # Kurze Pause

            cookies = driver.get_cookies()
            analysis_results = cookie_analysis(cookies, extracted_domain)

            logs = driver.get_log('browser')
            third_party_cookie_warnings, third_party_urls, extracted_urls = count_thirdparty_cookie_warnings(logs, extracted_domain)

            #collected alle ergebnisse row für row in die entsprechenden columns 
            results_df = results_df.append({
                'URL': url,
                'Domain': extracted_domain,
                'Persistent_Cookies': analysis_results['persistent_count'],
                'Session_Cookies': analysis_results['session_count'],
                'Different_Domain_Cookies': analysis_results['different_domain_count'],
                'Secure_Cookies': analysis_results['secure_count'],
                'HttpOnly_Cookies': analysis_results['http_only_count'],
                'SameSite_None_Cookies': analysis_results['same_site_none_count'],
                'Third_Party_Blocked': third_party_cookie_warnings,
                'External_URLs': list(third_party_urls),
                'CSP_Violations': extracted_urls
            }, ignore_index=True)

        except Exception as e:
            print(f'Fehler beim Zugriff auf {url}: {e}')

    driver.quit()

    # Speicher  DataFrame in ExcelDatei
    results_df.to_excel('cookie_analysis_results.xlsx', index=False)


browser_logging()



print(persistent_count_all) 
print(session_count_all)
print(different_domain_count_all)
print(secure_count_all)
print(http_only_count_all)
print(same_site_none_count_all)
print(third_party_blocked_count_all)






































            
# def undetected():
#     options = uc.ChromeOptions()

#     # Verhindert, dass Selenium als automatisierter Test erkannt wird
#     options.add_argument('--disable-blink-features=AutomationControlled')

#     driver = uc.Chrome(options=options)

#     with open('cookies.txt', 'w') as cookie_file:
#         for url in urls:
#             try:
#                 driver.get(url)
#                 # Warte einige Sekunden, um sicherzustellen, dass alle Cookies gesetzt wurden
#                 driver.implicitly_wait(10)

#                 cookies = driver.get_cookies()

#                 for cookie in cookies:
#                     # Schreibe Cookie-Details in die Datei, einschließlich der Domain
#                     cookie_file.write(f"Domain: {cookie['domain']}, Name: {cookie['name']}, Value: {cookie['value']}\n")

#             except Exception as e:
#                 print(f"Ein Fehler ist aufgetreten: {e}")
    	
#     driver.close()
#     driver.quit()


# def detected():
#     options = Options()

#     options.add_argument("--window-size=1920,1080")
#     options.add_argument("--headless")
#     driver = webdriver.Chrome(options=options)

#     with open('cookies_normal.txt', 'w') as cookie_file:
#         for url in urls:
#             try:
#                 driver.get(url)
#                 # Warte einige Sekunden, um sicherzustellen, dass alle Cookies gesetzt wurden
#                 driver.implicitly_wait(10)

#                 cookies = driver.get_cookies()

#                 for cookie in cookies:
#                     # Schreibe Cookie-Details in die Datei, einschließlich der Domain
#                     cookie_file.write(f"Domain: {cookie['domain']}, Name: {cookie['name']}, Value: {cookie['value']}\n")

#             except Exception as e:
#                 print(f"Ein Fehler ist aufgetreten: {e}")
    	
#     driver.close()
#     driver.quit()
