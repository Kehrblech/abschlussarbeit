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


persistent_count_all = 0
session_count_all = 0
different_domain_count_all = 0
secure_count_all = 0
http_only_count_all = 0
same_site_none_count_all = 0
third_party_blocked_count_all = 0 

#https://github.com/jkwakman/Open-Cookie-Database/blob/master/open-cookie-database.csv 
#Quelle aller Cookie bedeutungen nur ein paar "wichtige" und auch wirklich vorkommende 
def determine_cookie_purpose(cookie_name):
    known_cookies = {
        '_ga': 'Analytics - Used by Google Analytics to track user activity over different browsing sessions.',
        '_fbp': 'Advertising - Used by Facebook to deliver a series of advertisement products such as real time bidding from third party advertisers.',
        'PHPSESSID': 'Session Management - A session cookie sent by web servers to keep track of your browsing session.',
        '_cf_bm': 'Security - Used by Cloudflare to distinguish between humans and bots.',
        '__cfduid': 'Security - Used by Cloudflare to identify individual clients behind a shared IP address and apply security settings on a per-client basis.',
        '_gid': 'Analytics - Used by Google Analytics to distinguish users.',
        'JSESSIONID': 'Session Management - Used by server-side frameworks to manage a user session.',
        "__Secure-ENID": "Security - Used by Google to enhance security.",
        "AEC": "Security - Used to ensure browsing security by preventing cross-site request forgery.",
        "VISITOR_INFO1_LIVE": "YouTube cookie that measures your bandwidth to determine whether you get the new player interface or the old.",
        "YSC": "YouTube cookie that tracks views of embedded videos.",
        "PREF": "YouTube cookie that stores user preferences and other unspecified purposes.",
        "__Secure-YEC": "Security - Ties user’s activity to the device/IP to prevent fraud.",
        "ZFY": "Functionality - Used for site functionality purposes (exact purpose unknown).",
        "BA_HECTOR": "Analytics/Performance - Used to track user interaction and detect potential problems.",
        "BAIDUID_BFESS": "Identification - Baidu's user identification cookie.",
        "PSTM": "Preferences - Baidu's preference tracking cookie.",
        "BDORZ": "Functionality - Baidu's functionality cookie for user session identification.",
        "BIDUPSID": "Identification - Baidu's user identification cookie.",
        "SecureNetflixId": "Authentication - Used by Netflix for authentication purposes.",
        "OptanonConsent": "Compliance - Used by OneTrust for compliance with privacy laws.",
        "NetflixId": "Authentication - Used by Netflix to identify the user's session.",
        "nfvdid": "Functionality - Helps Netflix provide better recommendations.",
        "flwssn": "Session - Used by Netflix to identify the user's session.",
        "ai_session": "Analytics - Used by Microsoft Application Insights software to collect statistical usage and telemetry information.",
        "MUID": "Identification - Used by Microsoft as a unique identifier.",
        "mc": "Advertising/Tracking - Quantserve/Quantcast advertising cookie for tracking purposes.",
        "vuid": "Analytics - Used by Vimeo to collect analytics tracking information.",
        "muxData": "Analytics - Used by Mux to track video analytics information.",
        "sp_ab": "Feature Testing - Used by Spotify for feature testing.",
        "sp_landing": "Referral Tracking - Used by Spotify to track referral URLs.",
        "sp_t": "Analytics - Spotify analytics tracking.",
        "cf_clearance": "Security - Used by CloudFlare to identify individual clients behind a shared IP address and apply security settings per client.",
        "__cfruid": "Security - Cloudflare setting to identify trusted web traffic.",
        "datadome": "Security - Used by Datadome to provide bot protection.",
        "ak_bmsc": "Security - Used by Akamai to maintain security and protection from attacks.",
        "bwid": "Identification - Used to identify the end user persistently.",
        "everest_g_v2": "Tracking - Used by Everest Technologies for tracking purposes.",
        "gcl_au": "Ad Performance - Used by Google AdSense for experimenting with advertisement efficiency.",
        "_gat": "Throttling - Used by Google Analytics to throttle request rate.",
        "_gat_UA-XXXX": "Throttling - Used by Google Analytics to throttle request rate for the site's GA account.",
    
    }
    return known_cookies.get(cookie_name, 'Unknown')

#mit simplen regex browser log durchforsten und nach blocked messages suchen, zählen 
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
#fehler anfällig 
def extract_urls_from_csp(logs,main_domain):
    #soll 
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
    
    cookie_counts_by_purpose = {
        'Analytics': 0,
        'Advertising': 0,
        'Session Management': 0,
        'Security': 0,
        'Functionality': 0,
        'Preferences': 0,
        'Compliance': 0,
        'Other': 0
        #könnte auch tracking Cookies zählen aber die werden eh gefiltert von chrome
    }
    
    persistent_count = 0
    session_count = 0
    different_domain_count = 0
    secure_count = 0
    http_only_count = 0
    same_site_none_count = 0
    cookie_purposes = {}  #dict für die purposes zwecke, funktioniert gut 
    
    for cookie in cookies:
        #zähle persistent oder session
        if 'expiry' in cookie:
            persistent_count += 1
            persistent_count_all += 1
        else:
            session_count += 1
            session_count_all += 1
        #differenziere domains/ klappt nicht richtig bisschen schwachsinn
        if extracted_domain not in cookie['domain']:
            different_domain_count += 1
            different_domain_count_all += 1
        #zähle securte
        if cookie.get('secure'):
            secure_count += 1
            session_count_all += 1
        #zähle httponly
        if cookie.get('httpOnly'):
            http_only_count += 1
            http_only_count_all += 1
        #zähle same
        if cookie.get('sameSite') == 'None':
            same_site_none_count += 1
            same_site_none_count_all += 1
            
        #ab hier kompliziert    
        cookie_name = cookie['name']
        cookie_purpose = determine_cookie_purpose(cookie_name)
        #zweck ins dictionary, key ist cookie_name, value ist zweck
        cookie_purposes[cookie_name] = cookie_purpose
        
        main_purpose = cookie_purpose.split(' - ')[0]  # nur erster Teil trennen von beschreibenung
        #wenn anfang in purposes
        if main_purpose in cookie_counts_by_purpose:
            cookie_counts_by_purpose[main_purpose] += 1
        else:
            cookie_counts_by_purpose['Other'] += 1

    return {
        'persistent_count': persistent_count,
        'session_count': session_count,
        'different_domain_count': different_domain_count,
        'secure_count': secure_count,
        'http_only_count': http_only_count,
        'same_site_none_count': same_site_none_count,
        'cookie_purposes': cookie_purposes,
        'cookie_counts_by_purpose': cookie_counts_by_purpose
    }
    
def browser_logging():
    #WICHTIG aufbau des frames für das Excel Sheets COLOUMN weise! 
    results_df = pd.DataFrame(columns=['URL', 'Domain', 'Persistent_Cookies', 'Session_Cookies', 'Different_Domain_Cookies', 'Secure_Cookies', 'HttpOnly_Cookies', 'SameSite_None_Cookies', 'Third_Party_Blocked', 'External_URLs', 'CSP_Violations', 'Purposes', 'Analytics_Cookies', 'Advertising_Cookies', 'Session_Management_Cookies', 'Security_Cookies', 'Functionality_Cookies', 'Preferences_Cookies', 'Compliance_Cookies', 'Other_Cookies'])
    # Chrome zusammenbasteln Mehr optiopnen hinzufügen 
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')  #Ignoriert SSL
    options.add_argument('--ignore-certificate-errors')  #Ignoriert Zertifikatsfehler

    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    #beinhaltet nur .com domains und .org 
    com_domains = [
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
    'https://www.uber.com/', #Ab hier neue 
    'https://www.lyft.com/',
    'https://www.airbnb.com/',
    'https://www.booking.com/',
    'https://www.trivago.com/',
    'https://www.opentable.com/',
    'https://www.zomato.com/',
    'https://www.doordash.com/',
    'https://www.grubhub.com/',
    'https://www.ubereats.com/',
    'https://www.expedia.com/',
    'https://www.kayak.com/',
    'https://www.priceline.com/',
    'https://www.hotwire.com/',
    'https://www.tripadvisor.com/',
    'https://www.orbitz.com/',
    'https://www.travelocity.com/',
    'https://www.cheapoair.com/',
    'https://www.flightaware.com/',
    'https://www.skyscanner.com/',
    'https://www.agoda.com/',
    'https://www.hotels.com/',
    'https://www.homeaway.com/',
    'https://www.vrbo.com/',
    'https://www.couchsurfing.com/',
    'https://www.hostelworld.com/',
    'https://www.lonelyplanet.com/',
    'https://www.roughguides.com/',
    'https://www.fodors.com/',
    'https://www.frommers.com/'
    ]
    
    de_domains = [
    'https://www.adlermode.de',
    'https://www.alternate.de',
    'https://www.apo-rot.de',
    'https://www.apotal.de',
    'https://www.bahnhof-apotheke.de',
    'https://www.baur.de',
    'https://www.bergfreunde.de',
    'https://www.betten.de',
    'https://www.bike24.de',
    'https://www.buecher.de',
    'https://www.cewe.de',
    'https://www.conrad.de',
    'https://www.cyberport.de',
    'https://www.docmorris.de',
    'https://www.edeka.de',
    'https://www.elektroshopwagner.de',
    'https://www.emp.de',
    'https://www.engelhorn.de',
    'https://www.erwinmueller.de',
    'https://www.esprit.de',
    'https://www.eventim.de',
    'https://www.flaconi.de',
    'https://www.galeria.de',
    'https://www.hagebau.de',
    'https://www.hornbach.de',
    'https://www.jako-o.de',
    'https://www.kfzteile24.de',
    'https://www.mediamarkt.de',
    'https://www.medpex.de',
    'https://www.notebooksbilliger.de',
    'https://www.obi.de',
    'https://www.pearl.de',
    'https://www.saturn.de',
    'https://www.schecker.de',
    'https://www.schuhcenter.de',
    'https://www.shop-apotheke.com',
    'https://www.thalia.de',
    'https://www.tirendo.de',
    'https://www.voelkner.de',
    'https://www.westfalia.de',
    'https://www.apotheken-umschau.de',
    'https://www.bahnhof.de',
    'https://www.berliner-volksbank.de',
    'https://www.bmw.de',
    'https://www.dat.de',
    'https://www.deutschepost.de',
    'https://www.dkb.de',
    'https://www.douglas.de',
    'https://www.duden.de',
    'https://www.eurowings.de',
    'https://www.fielmann.de',
    'https://www.finanzen.net',
    'https://www.fitx.de',
    'https://www.fluege.de',
    'https://www.gamestop.de',
    'https://www.ikea.de',
    'https://www.kaufland.de',
    'https://www.lego.com/de-de',
    'https://www.lidl.de',
    'https://www.metro.de',
    'https://www.mydays.de',
    'https://www.pixum.de',
    'https://www.rewe.de',
    'https://www.schwab.de',
    'https://www.steiff.com/de-de',
    'https://www.tchibo.de',
    'https://www.toom.de',
    'https://www.spiegel.de',
    'https://www.bild.de',
    'https://www.faz.net',
    'https://www.zeit.de',
    'https://www.tagesspiegel.de',
    'https://www.zdf.de',
    'https://www.heise.de',
    'https://www.golem.de',
    'https://www.chip.de',
    'https://www.computerbild.de',
    'https://www.auto-motor-und-sport.de',
    'https://www.sport1.de',
    'https://www.kicker.de',
    'https://www.transfermarkt.de',
    'https://www.stern.de',
    'https://www.focus.de',
    'https://www.gmx.net',
    'https://www.web.de',
    'https://www.amazon.de',
    'https://www.zalando.de',
    'https://www.rosenheim24.de',
    'https://www.merkur.de',
    'https://www.stuttgarter-zeitung.de',
    'https://www.stuttgarter-nachrichten.de',
    'https://www.br.de',
    'https://www.mdr.de',
    'https://www.wdr.de',
    'https://www.rbb-online.de',
    'https://www.lufthansa.com',
    'https://www.daserste.de',
    'https://www.dw.de',
    'https://www.ardmediathek.de',
    'https://www.zdfmediathek.de',
    'https://www.phoenix.de',
    'https://www.arte.tv/de',
    'https://www.3sat.de',
    'https://www.prosieben.de',
    'https://www.sat1.de',
    'https://www.kabeleins.de',
    'https://www.vox.de',
    'https://www.rtl.de',
    'https://www.ntv.de',
    'https://www.xing.de',
    'https://www.stepstone.de',
    'https://www.immobilienscout24.de',
    'https://www.autoscout24.de',
    'https://www.mobile.de',
    'https://www.chefkoch.de',
    'https://www.stayfriends.de',
    'https://www.kununu.de',
    'https://www.dkb.de',
    'https://www.comdirect.de',
    'https://www.ing.de',
    'https://www.check24.de',
    'https://www.verivox.de',
    'https://www.idealo.de',
    'https://www.mydealz.de',
    'https://www.heise.de/newsticker',
    'https://www.computerbase.de',
    'https://www.giga.de',
    'https://www.gamestar.de',
    'https://www.spieletipps.de',
    'https://www.netflix.de',
    'https://www.amazon.de/prime',
    'https://www.maxdome.de',
    'https://www.sky.de',
    'https://www.dazn.de',
    'https://www.disneyplus.de',
    'https://www.joyn.de',
    'https://www.tvnow.de',
    'https://www.eurosport.de',
    'https://www.sport1.de',
]

    
    test_domains = [
        'https://www.check24.de',
        'https://www.verivox.de',
        'https://www.idealo.de',
        'https://www.mydealz.de',
        'https://www.heise.de/newsticker',
        'https://www.computerbase.de',
        'https://www.giga.de',
        'https://www.gamestar.de',
        'https://www.spieletipps.de',
        'https://www.amazon.de/prime',
        'https://www.maxdome.de',
        'https://www.sky.de',
        'https://www.rwu.de',
        'https://www.pizzafarm.pizza',
    ]

    #nicht vergessen auch Actions Performen auf der Seite um "legit" auszusehen.
    for url in de_domains:
        #Initialisiere extr_urls um fehler abfangen vergesse oder übersehe irgendwas... egal unwichtig
        extracted_urls = []  
        try:
            #  
            driver.get(url)
            parsed_url = urlparse(url)
            current_domain = parsed_url.netloc
            #Fehler anfällig verbessern
            extracted_domain = tldextract.extract(current_domain).registered_domain
            # interaktinon perfomen 
            # actions = ActionChains(driver)
            # actions.move_to_element(wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))).perform()
            try:
                # Warte auf sichtbarkeit  max 10 
                target_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.TAG_NAME, "body"))
                )#then perfrom 
                actions = ActionChains(driver)
                actions.move_to_element(target_element).perform()
                
                print("Element gefunden und Aktion ausgeführt!")
                
                # #klick performance
                # button = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.ID, "deinButtonId"))
                # )
                # button.click()
                # print("Weitere Aktion erfolgreich ausgeführt.")
            except EC:
                print("Element nicht gefunden!!!")
            time.sleep(1) 

            cookies = driver.get_cookies()

            analysis_results = cookie_analysis(cookies, extracted_domain)
            # logs nach warnungen durchsuchen 
            logs = driver.get_log('browser')
            third_party_cookie_warnings, third_party_urls, extracted_urls = count_thirdparty_cookie_warnings(logs, extracted_domain)
            
            #collected alle ergebnisse row für row in die entsprechenden columns 
            new_row = {
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
                'CSP_Violations': extracted_urls,
                'Purposes':analysis_results['cookie_purposes'],
                'Analytics_Cookies': analysis_results['cookie_counts_by_purpose'].get('Analytics', 0),
                'Advertising_Cookies': analysis_results['cookie_counts_by_purpose'].get('Advertising', 0),
                'Session_Management_Cookies': analysis_results['cookie_counts_by_purpose'].get('Session Management', 0),
                'Security_Cookies': analysis_results['cookie_counts_by_purpose'].get('Security', 0),
                'Functionality_Cookies': analysis_results['cookie_counts_by_purpose'].get('Functionality', 0),
                'Preferences_Cookies': analysis_results['cookie_counts_by_purpose'].get('Preferences', 0),
                'Compliance_Cookies': analysis_results['cookie_counts_by_purpose'].get('Compliance', 0),
                'Other_Cookies': analysis_results['cookie_counts_by_purpose'].get('Other', 0)

            }
            #  abspeichern in dataFrame row f+ür row 
            results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)

        except Exception as e:
            print(f'Fehler zugriff {url}: {e}')

    driver.quit()

    # speicher als excel
    results_df.to_excel('cookie_analysis_results.xlsx', index=False)

browser_logging()
