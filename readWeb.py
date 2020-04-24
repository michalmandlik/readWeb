from typing import List, Any
from bs4 import BeautifulSoup
from selenium import webdriver
import random
# The first step is always the same: import all necessary components:
import smtplib
from email.mime.text import MIMEText
import time

from socket import gaierror

# version = 1.1.0.0

# log version 1.1.0.0
# added multiple pages

sleepTime = 600     # [s]
cntChecker = 0
NUM_CHECKER = 5     # num iteration before control email is sent

# debug mode
DEBUG_MODE = 0  # enable the prints and add extra item to the offer list

# fileName
fileName = 'offers.log'

# maximum number of pages
MAX_NUM_PAGES = 5

url = "https://www.sreality.cz/hledani/prodej/byty/praha-7?velikost=2%2Bkk,2%2B1,1%2B1,3%2Bkk&cena-od=0&cena-do=7000000&bez-aukce=1"

while True:

    cntChecker = cntChecker + 1
    time.sleep(sleepTime)
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)

    # get information from sreality
    #driver = webdriver.Safari()     # TODO support only Safari browser
    #driver = webdriver.Firefox()
    #driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    #driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.

    for cntPage in range(MAX_NUM_PAGES):
        # get information from sreality
        driver = webdriver.Safari()  # TODO support only Safari browser
        if cntPage == 0:
            # driver.get("https://www.sreality.cz/hledani/prodej/byty/brno?stari=mesic")
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
        else:
            url = url + "&strana=" + str(cntPage)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        listCurrentOffers = []          # list of current offers
        numCurrentOffers = 0            #
        for title in soup.select(".text-wrap"):
            numCurrentOffers = numCurrentOffers + 1
            num = "https://www.sreality.cz" + title.select_one(".title").get('href')
            listCurrentOffers.append(num)

    # load data from a log
    with open(fileName) as f:       # TODO issue once the file doesn't exist
        listLoggedData = f.read().splitlines()

    # compare log against current loaded data
    listNewOffers = []      # offers which are not in the offers.log
    for currentItem in listCurrentOffers:
        isInTheList = 0      # set the flag to 0 as default value
        for loggedItem in listLoggedData:
            # compare strings
            isEqual = currentItem == loggedItem
            if isEqual:
                isInTheList = 1     # if the item is in the list

        if not isInTheList:
            listNewOffers.append(currentItem)

    # update log
    if listNewOffers:
        print('New offer(s) found')

        # save new offers to the log file
        f = open(fileName, 'a')
        f.write('\n')
        s1 = '\n'.join(listNewOffers)
        f.write(s1)
        f.close()

        # send an email
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.ehlo()

        # start TLS for security
        s.starttls()
        # Authentication
        s.login("mmachecker@gmail.com", "klokanBarezi")
        # message to be sent
        outS = '\n'.join(listNewOffers)
        msg = MIMEText(outS)
        msg['Subject'] = 'Nove reality'
        msg['From'] = 'mmaChecker@gmail.com'
        msg['To'] = 'michalmandlik@gmail.com'
        # sending the mail
        s.sendmail("mmachecker@gmail.com", "michalmandlik@gmail.com", msg.as_string(msg))
        # terminating the session
        s.quit()
        print('Email with offers sent')

    if cntChecker == NUM_CHECKER:
        cntChecker = 0
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.ehlo()

        # start TLS for security
        s.starttls()

        # Authentication
        s.login("mmachecker@gmail.com", "klokanBarezi")

        # message to be sent
        outS = 'Safari checker is running'
        msg = MIMEText(outS)
        msg['Subject'] = 'Safari checker is running'
        msg['From'] = 'mmaChecker@gmail.com'
        msg['To'] = 'michalmandlik@gmail.com'

        # sending the mail
        s.sendmail("mmachecker@gmail.com", "michalmandlik@gmail.com", msg.as_string(msg))

        # terminating the session
        s.quit()