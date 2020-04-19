from typing import List, Any
from bs4 import BeautifulSoup
from selenium import webdriver
import random
# The first step is always the same: import all necessary components:
import smtplib
from email.mime.text import MIMEText
from socket import gaierror

#debug mode
DEBUG_MODE = 1

#fileName
fileName = 'offers.log'

# get information from sreality
driver = webdriver.Safari()

# driver.get("https://www.sreality.cz/hledani/prodej/byty/brno?stari=mesic")
driver.get(
    "https://www.sreality.cz/hledani/prodej/byty/praha-7?velikost=2%2Bkk,2%2B1,1%2B1,3%2Bkk&cena-od=0&cena-do=7000000&bez-aukce=1")
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

listCurrentOffers = []      # list of current offers
numCurrentOffers = 0           #
for title in soup.select(".text-wrap"):
    numCurrentOffers = numCurrentOffers + 1
    num = "https://www.sreality.cz" + title.select_one(".title").get('href')
    listCurrentOffers.append(num)
    #print(num)

#print(numCurrentOffers)
#print(listCurrentOffers)

# debug mode
if DEBUG_MODE:
    numCurrentOffers = numCurrentOffers + 1
    listCurrentOffers.append(str(random.random()))




# load data from a log
with open(fileName) as f:
    listLoggedData = f.read().splitlines()

print(listLoggedData)
print(listCurrentOffers)

# compare log against current loaded data
listNewOffers = []      # offers which are not in the offers.log
for currentItem in listCurrentOffers:
    isInTheList = 0      # set the flag to 0 as default value
    for loggedItem in listLoggedData:
        # compare strings
        isEqual = currentItem == loggedItem
        if isEqual:
            isInTheList = 1     # if the item is in the list

    if not(isInTheList):
        print('Item ', currentItem, ' is not in the logged list')
        listNewOffers.append(currentItem)
    else:
        print('Item ', currentItem, ' is in the logged list')

print()
#print(listNewOffers)

# update log
if listNewOffers:
    print('New offers')

    # tmp for now - save current offers to the log
    f = open(fileName, 'w')
    s1 = '\n'.join(listCurrentOffers)
    f.write(s1)
    f.close()
else:
    print('No new offers')

if 0:
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("mmachecker@gmail.com", "klokanBarezi")

    # message to be sent

    outS = '     '.join(listCurrentOffers)
    msg = MIMEText(outS)
    msg['Subject'] = 'Nove reality'
    msg['From'] = 'mmaChecker@gmail.com'
    msg['To'] = 'michalmandlik@gmail.com'

    # sending the mail
    s.sendmail("mmachecker@gmail.com", "michalmandlik@gmail.com", msg.as_string(msg))

    # terminating the session
    s.quit()
