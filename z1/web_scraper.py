from bs4 import BeautifulSoup
import traceback
import requests
import threading
import random
import mysql.connector
import time
import re


PROXY_TIMEOUT_SECONDS = 60
NUMBER_OF_CHECKING_THREADS = 200
NUMBER_OF_SCRAPING_THREADS = 300
WANTED_NUMBER_OF_CARS = 30000

proxyList = []
usedHTTPsProxies = []
threadList = []

def getNumberOfCarsInDatabase():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )

        connection.autocommit = True
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT COUNT(*) FROM AUTOMOBILI")
        numberOfEntries = cursor.fetchall()
        cursor.close()
        connection.close()

        return (numberOfEntries[0][0])
    except Exception as e:
        return -1

def carExistsWithinDatabase(id):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )

        connection.autocommit = True
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT COUNT(*) FROM AUTOMOBILI WHERE idOglasa = %s", (id,))
        numberOfEntries = cursor.fetchall()
        cursor.close()
        connection.close()

        return (numberOfEntries[0][0])
        print(numberOfEntries[0][0])
    except Exception as e:
        print(e)
        return -1

def insertCarIntoDatabase(idOglasa, cena, stanje, marka, model, godiste, kilometraza, karoserija, gorivo, kubikaza, snagaMotora, menjac, brojVrata, boja, lokacijaProdavca):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )
        connection.autocommit = True
        cursor = connection.cursor(buffered=True)
        cursor.execute("INSERT INTO AUTOMOBILI (idOglasa, cena, stanje, marka, model, godiste, kilometraza, karoserija, gorivo, kubikaza, snagaMotora, menjac, brojVrata, boja, lokacijaProdavca) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (idOglasa, cena, stanje, marka, model, godiste, kilometraza, karoserija, gorivo, kubikaza, snagaMotora, menjac, brojVrata, boja, lokacijaProdavca))
        cursor.close()
        connection.close()
        return 0
    except Exception as e:
        return -1


numOfEntires = getNumberOfCarsInDatabase()
if numOfEntires == -1:
    print("[-] Database doesn't exist. Create the database before running the scraper.")
    exit()

headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0 "
}


workingProxiesMutex = threading.Lock()
printMutex = threading.Lock()

# class proxyCheckingThread(threading.Thread):
#     def __init__(self, proxy, timeout):
#         super(proxyCheckingThread, self).__init__()
#         self.proxy = proxy
#         self.timeout = timeout

#     def run(self):
#         global workingProxiesMutex
#         global printMutex
#         global usedHTTPsProxies
#         try:
#             response = requests.get(f"https://www.polovniautomobili.com", proxies={"https":self.proxy}, timeout=self.timeout, headers=headers)

#             if response.status_code == 200:
#                 workingProxiesMutex.acquire()
#                 usedHTTPsProxies.append(self.proxy)
#                 workingProxiesMutex.release()

#                 printMutex.acquire()
#                 print(f"[+] HTTPs proxy [{self.proxy}] is working!")
#                 printMutex.release()
#             else:
#                 printMutex.acquire()
#                 print(f"[-] HTTPs proxy [{self.proxy}] is not working (status code={response.status_code}).")
#                 printMutex.release()
#         except:
#             printMutex.acquire()
#             print(f"[-] HTTPs proxy [{self.proxy}] is not working (timeout).")
#             printMutex.release()


fileProxies = open("proxies.txt", "r")
allLines = fileProxies.readlines()
fileProxies.close()

# for line in allLines:
#     proxyList.append(line.strip())

# print(f"[i] Checking input proxies for valid HTTPs proxies...")

# for p in proxyList:
#     if(len(threadList)) >= NUMBER_OF_CHECKING_THREADS:
#         for t in threadList:
#             t.join()
#         del threadList[:]
#     t = proxyCheckingThread(p, PROXY_TIMEOUT_SECONDS)
#     threadList.append(t)
#     t.start()

# for t in threadList:
#     t.join()

# del threadList[:]
# del proxyList[:]

for line in allLines:
    usedHTTPsProxies.append(line.strip())

usedHTTPsProxies.append("")


print(f"Number of used HTTPs proxies: {len(usedHTTPsProxies)}.")
print("")

def getNextProxy():
    result = ""
    if (len(usedHTTPsProxies) > 0):
        result = usedHTTPsProxies.pop(0)
        usedHTTPsProxies.append(result)
    return result


nizAutomobila = []
page=1

WANTED_NUMBER_OF_CARS = WANTED_NUMBER_OF_CARS - numOfEntires
if(WANTED_NUMBER_OF_CARS == 0):
    print(f"[i] Already enough cars ({numOfEntires}) exist within database.")
    exit()

if(NUMBER_OF_SCRAPING_THREADS > WANTED_NUMBER_OF_CARS): NUMBER_OF_SCRAPING_THREADS = WANTED_NUMBER_OF_CARS

# proxy = getNextProxy()
proxy = ""
success = False

while len(nizAutomobila) < WANTED_NUMBER_OF_CARS:
    print(f"[+] Enumerating all cars from page {page} (collected {len(nizAutomobila)}/{WANTED_NUMBER_OF_CARS}).")
    number = re.compile(r"[^\d]+")

    while not success:
        try:
            response = requests.get(f"https://www.polovniautomobili.com/auto-oglasi/pretraga?page={page}&sort=basic&city_distance=0&showOldNew=all&without_price=1", headers=headers, proxies={"https":proxy}, timeout=PROXY_TIMEOUT_SECONDS)
            if(response.status_code == 200):
                success=True
            else:
                print(f"[-] Error invalid response from web page - status code {response.status_code}")
                # proxy = getNextProxy()
                proxy = ""
                if(proxy != ""): print("[+] Switched to a new HTTPs proxy [" + proxy + "]." )
                else: print("[i] No available proxies remaining, using direct connection...")
        except:
            print(f"[-] Error while connecting (timeout).")
            # proxy = getNextProxy()
            proxy = ""
            if(proxy != ""): print("[+] Switched to a new HTTPs proxy [" + proxy + "]." )
            else: print("[i] No available proxies remaining, using direct connection...")

    success = False
    websiteHTML = response.text
    soup = BeautifulSoup(websiteHTML, "lxml")
    automobiliNaStranici = soup.find_all("article")
    
    
    for automobil in automobiliNaStranici:
        link = automobil.find("a", class_="firstImage")
        if link is not None:
            if (str("https://www.polovniautomobili.com" + link["href"]) not in nizAutomobila) and ((carExistsWithinDatabase(("https://www.polovniautomobili.com" + link["href"]).split("/")[4]))==0):
                nizAutomobila.insert(len(nizAutomobila), "https://www.polovniautomobili.com" + link["href"])
                if len(nizAutomobila) >= WANTED_NUMBER_OF_CARS: break
    page+=1





requests.packages.urllib3.disable_warnings()
carLinksMutex = threading.Lock()

class CarScrapingThread(threading.Thread):
    def __init__(self, id):
        super(CarScrapingThread, self).__init__()
        self.id = id
    def run(self):
        global workingProxiesMutex
        global printMutex
        global nizAutomobila
        global carLinksMutex

        workingProxiesMutex.acquire()
        self.proxy = getNextProxy()
        workingProxiesMutex.release()


        carLinksMutex.acquire()
        self.carLink = nizAutomobila.pop(0)
        numberOfRemainingCarLinks = len(nizAutomobila)
        carLinksMutex.release()

        while numberOfRemainingCarLinks > 0:
            try:
                response = requests.get(self.carLink, headers=headers, proxies={"https":self.proxy}, timeout=PROXY_TIMEOUT_SECONDS, verify=False)

                if response.status_code == 200:

                    websiteHTML = response.text
                    soup = BeautifulSoup(websiteHTML, "lxml")

                    cena = 0
                    stanje = ""
                    marka = ""
                    model = ""
                    godiste = 0
                    kilometraza = 0
                    karoserija = ""
                    gorivo = ""
                    kubikaza = 0
                    snagaMotora = 0
                    menjac = ""
                    brojVrata = 0
                    boja = ""
                    lokacijaProdavca = ""
                    idOglasa = self.carLink.split("/")[4]


                    number = re.compile(r"[^\d]+")
                    cenaText = soup.find_all("span", class_="priceClassified")
                    if(len(cenaText) == 0):
                        printMutex.acquire()
                        print(f"[-] Scraping Thread {self.id} - Could not get price of car [{self.carLink}].")
                        printMutex.release()

                        carLinksMutex.acquire()
                        if(len(nizAutomobila) > 0): self.carLink = nizAutomobila.pop(0)
                        numberOfRemainingCarLinks = len(nizAutomobila)
                        carLinksMutex.release()
                        continue
                    else: cena = number.sub("", cenaText[0].text)


                    foundItems = soup.find_all("div", class_="divider")
                    for item in foundItems:
                        text1 = item.find("div", class_="uk-width-1-2").text
                        text2 = item.find("div", class_="uk-width-1-2 uk-text-bold").text

                        if(text1 == "Stanje:"): stanje = text2
                        elif(text1 == "Marka"): marka = text2
                        elif(text1 == "Model"): model = text2
                        elif(text1 == "Godište"): godiste = number.sub("", text2)
                        elif(text1 == "Kilometraža"): kilometraza = number.sub("", text2)
                        elif(text1 == "Karoserija"): karoserija = text2
                        elif(text1 == "Gorivo"): gorivo = text2
                        elif(text1 == "Kubikaža"): kubikaza = int(number.sub("", text2))/10
                        elif(text1 == "Snaga motora"): snagaMotora = number.sub("", text2.split("/")[1])
                        elif(text1 == "Menjač"): menjac = text2
                        elif(text1 == "Broj vrata"): brojVrata = number.sub("", text2.split("/")[0])
                        elif(text1 == "Boja"): boja = text2

                    i = 0
                    foundItems = soup.find_all("div", class_="uk-grid uk-margin-top-remove")

                    for item in foundItems:
                        if(i == 1):  
                            lokacijaProdavca = (item.find("div", class_="uk-width-1-2")).find(text=True, recursive=False).lstrip()
                        i += 1

                    if(cena == "" or cena == 0 or stanje == "" or marka == "" or model == "" or godiste == 0 or kilometraza == 0 or karoserija == "" or gorivo == "" or kubikaza == 0 or snagaMotora == 0 or menjac == "" or brojVrata == 0 or boja == "" or lokacijaProdavca == ""):
                        printMutex.acquire()
                        print(f"[-] Scraping Thread {self.id} - Could not collect all data of car [{self.carLink}].")
                        printMutex.release()

                        carLinksMutex.acquire()
                        if(len(nizAutomobila) > 0): self.carLink = nizAutomobila.pop(0)
                        numberOfRemainingCarLinks = len(nizAutomobila)
                        carLinksMutex.release()
                        continue

                    if(insertCarIntoDatabase(idOglasa, cena, stanje, marka, model, godiste, kilometraza, karoserija, gorivo, kubikaza, snagaMotora, menjac, brojVrata, boja, lokacijaProdavca) != 0 ):
                        printMutex.acquire()
                        print(f"[-] Scraping Thread {self.id} - Error while inserting car into database [{self.carLink}]!")
                        printMutex.release()
                        carLinksMutex.acquire()
                        if(len(nizAutomobila) > 0): self.carLink = nizAutomobila.pop(0)
                        numberOfRemainingCarLinks = len(nizAutomobila)
                        carLinksMutex.release()
                        continue
                    
                    printMutex.acquire()
                    print(f"[+] Scraping Thread {self.id} - Successfully scraped car from link [{self.carLink}]!")
                    printMutex.release()

                    carLinksMutex.acquire()
                    if(len(nizAutomobila) > 0): self.carLink = nizAutomobila.pop(0)
                    numberOfRemainingCarLinks = len(nizAutomobila)
                    carLinksMutex.release()
                else:
                    printMutex.acquire()
                    if(self.proxy != ""): print(f"[-] Thread {self.id} - HTTPs proxy [{self.proxy}] is not working (status code={response.status_code}).")
                    else: print(f"[-] Scraping Thread {self.id} - Couldn't connect without a proxy (status code={response.status_code}).")
                    printMutex.release()

                    workingProxiesMutex.acquire()
                    self.proxy = getNextProxy()
                    workingProxiesMutex.release()

            except Exception as e:
                printMutex.acquire()
                # traceback.print_exc()
                # print(e)
                # print(self.carLink)
                if(self.proxy != ""): print(f"[-] Scraping Thread {self.id} - HTTPs proxy [{self.proxy}] is not working (timeout).")
                else: print(f"[-] Scraping Thread {self.id} - Couldn't connect without a proxy (timeout).")
                printMutex.release()

                workingProxiesMutex.acquire()
                self.proxy = getNextProxy()
                workingProxiesMutex.release()
            
            time.sleep(5)

        printMutex.acquire()
        print(f"[i] Scraping Thread {self.id} -  finished execution.")
        printMutex.release()



for x in range(NUMBER_OF_SCRAPING_THREADS):
    t = CarScrapingThread(x)
    threadList.append(t)
    t.start()

for t in threadList:
    t.join()

del threadList[:]

print("[+] Scraper finished.")