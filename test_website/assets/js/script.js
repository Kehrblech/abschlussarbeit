function sendDataToServer(data) {
    // aus Proof of Concept gründen keine Verschlüsselung und kein HTTPS, bitte um verständnis
    fetch('http://127.0.0.1:5000/api/save-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'

        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => console.log('Daten erfolgreich gesendet:', data))
        .catch((error) => console.error('Fehler beim Senden der Daten:', error));
}
//Struct
let collectedData = {
    clicks: [],
    scrollPercentage: 0,
    scrollMax: 0,
    scrollData: {},
    time: [],
    sectionVisibility: {},
    userAgent: {},
    url: {},
    historyLength: 0,
    screenWidth: 0,
    screenHeight: 0,
    device: {},
    timezone: {},
    cookies: {},
    connectionSpeed: {},
    noTracking: {},
    userAgentLanguage: {},
    cpuCores: {},
    referrer: {},

};

let lastScrollPosition = 0;
let lastScrollTime = Date.now();
let entryTime = Date.now();
let unloadTime = 0;
let domTime = 0;
let maxScrollPercentage = 0;
let maxScroll = document.documentElement.scrollHeight - window.innerHeight;
collectedData.scrollPercentage = maxScrollPercentage;
collectedData.scrollMax = maxScroll;
let visibleSections = {}; //Wichtig für die Sektuionsspeicherung weiter unten updateVisibileTime() handleIntersection()



//Erstellen eines EventListener,
//der Mouse Clicks registriert. 
document.addEventListener('click', function (e) {
    clickPosition(e)
});

//Funktion die vom EventListener aufgerufen wird,
//sobald ein Mouse Click registriert wird.
function clickPosition(e) {
    //Struct aufruf zum speichern der Click daten.
    collectedData.clicks.push({
        x: e.pageX,
        y: e.pageY,
        time: Date.now(),
        element: e.target.tagName
     });
}   

//ausrechnung scroll zeit in sec zum späteren addierne 
function updateScrollTime() {
    let currentTime = Date.now();
    //in sec umrechnung 
    let timeSpent = (currentTime - lastScrollTime) / 1000;

    if (!collectedData.scrollData[lastScrollPosition]) {
        collectedData.scrollData[lastScrollPosition] = 0;
    }
    collectedData.scrollData[lastScrollPosition] += timeSpent;

    lastScrollTime = currentTime;
}



window.addEventListener('scroll', function () {
    updateVisibleTime();
    updateScrollTime();
    lastScrollPosition = window.scrollY;
});
//!!!!!!!
//!!!!!!!Wichtig wenn client verlässt wird unsere collectedData mit POSt an Flask API geschickt!!!!!!!!
//!!!!!!!
// window.addEventListener('beforeunload', function () {

//     collectedData.time.push({ "entry": entryTime, "leave": Date.now(), "domLoadingTime": domTime });
//     collectedData.scrollPercentage = maxScrollPercentage;
//     sendDataToServer(collectedData);
//     navigator.sendBeacon('http://127.0.0.1:5000/api/save-data', JSON.stringify(collectedData));
// });
// document.addEventListener("visibilitychange", function () {
//     if (document.visibilityState === "visible") {

//     } else {
//         collectedData.time.push({ "entry": entryTime, "leave": Date.now(), "domLoadingTime": domTime });
//         collectedData.scrollPercentage = maxScrollPercentage;
//         sendDataToServer(collectedData);
//     }
// });

let debounceTimeout;

function handleKeyDown(event) {
    if (event.key === 'Enter' || event.keyCode === 13) {
        event.preventDefault();

        // Vorherige Debounce-Timeouts löschen
        clearTimeout(debounceTimeout);

        // Neue Debounce-Timeout setzen
        debounceTimeout = setTimeout(() => {
            event.preventDefault(); // Verhindert Standardaktionen

            // Ihre Logik zum Sammeln von Daten
            collectedData.time.push({ "entry": entryTime, "leave": Date.now(), "domLoadingTime": domTime });
            collectedData.scrollPercentage = maxScrollPercentage;

            // Senden der Daten an den Server
            sendDataToServer(collectedData);
            navigator.sendBeacon('http://127.0.0.1:5000/api/save-data', JSON.stringify(collectedData));

            isDataSent = true; // Aktualisieren der Kontrollvariable
        }, 500); // 500 Millisekunden Debounce-Zeit
    }
}

document.addEventListener('keydown', handleKeyDown);
document.addEventListener('DOMContentLoaded', function () {
    domTime = Date.now();
    collectedData.userAgent = navigator.userAgent;
    collectedData.historyLenght = history.length;
    collectedData.url = window.location.href;
    collectedData.screenWidth = screen.width;
    collectedData.screenHeight = screen.height;
    collectedData.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    collectedData.cookies = navigator.cookieEnabled;
    collectedData.connectionSpeed = navigator.connection && navigator.connection.effectiveType;
    collectedData.noTracking = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack;
    collectedData.userAgentLanguage = navigator.language || navigator.userLanguage;
    console.log(navigator.language)
    console.log(navigator.userLanguage)
    collectedData.cpuCores = navigator.hardwareConcurrency || "Nicht verfügbar";
    collectedData.referrer = document.referrer || "Direkter Zugriff";
});

// Nicht notwendig kann auch Server aber als Proof of Con. und vorallem falls klick oder scroll daten umgerechnet und angepasst werden müssen
function isMobile() {
    var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    if (isMobile) {
        collectedData.device = isMobile;
    } else {
        collectedData.device = isMobile;
    }
}


function handleIntersection(entries, observer) {
    entries.forEach(entry => {

        let sectionId = entry.target.id;
        if (entry.isIntersecting) {
            //1.start beobachtung
            visibleSections[sectionId] = visibleSections[sectionId] || Date.now();
        } else {
            // 2. wenn ende der Beobachtung 
            if (visibleSections[sectionId]) {
                // 3. ende beobachtung datum jetzt mit start datum abziehen
                let timeVisible = Date.now() - visibleSections[sectionId];
                // 4. !TODO fallas dataset noch keine eintrag mach eintrag
                if (!collectedData.sectionVisibility[sectionId]) {
                    collectedData.sectionVisibility[sectionId] = 0;
                }
                //5. +=speichern time 
                collectedData.sectionVisibility[sectionId] += timeVisible;
                // console.log(`Section ${sectionId} now invisible, visible time insec: ${collectedData.sectionVisibility[sectionId]}`);
                //5.1 freigeben
                delete visibleSections[sectionId];
            }
        }
    });
}
//gleich wie obere fubnktion diesmal nur mit scroll event trigger
function updateVisibleTime() {
    let currentTime = Date.now();

    for (let sectionId in visibleSections) {
        //Überprüfe auf gültigkeit 
        if (visibleSections.hasOwnProperty(sectionId)) {
            let timeVisible = currentTime - visibleSections[sectionId];
            if (!collectedData.sectionVisibility[sectionId]) {
                collectedData.sectionVisibility[sectionId] = 0;
            }
            collectedData.sectionVisibility[sectionId] += timeVisible;
            visibleSections[sectionId] = currentTime; // zurücksetzetn für nächste berechnung 
            // console.log(`!Section ${sectionId} updated time: ${collectedData.sectionVisibility[sectionId]}`);

        }
    }
}

let observer = new IntersectionObserver(handleIntersection, { threshold: [0.0] });

document.querySelectorAll('section').forEach(section => {

    observer.observe(section);
});

window.addEventListener('scroll', updateVisibleTime);

window.addEventListener('scroll', function () {
    let scrollPosition = window.scrollY || document.documentElement.scrollTop;
    maxScrollPostion(scrollPosition);

});

//calculate max scroll Pos. for each clietn
function maxScrollPostion(position) {
    let scrollPercentage = (position / maxScroll) * 100;
    if (maxScrollPercentage < scrollPercentage) {
        maxScrollPercentage = scrollPercentage;
    }
}
//debounce um nicht browser zu überfordern 
function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this, args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

window.addEventListener('scroll', debounce(function () {
    updateVisibleTime();
    updateScrollTime();
    lastScrollPosition = window.scrollY;
}, 100)); // 100ms sekunden debounce um nicht browser zu überfordern 
