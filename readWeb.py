from bs4 import BeautifulSoup
from selenium import webdriver
# The first step is always the same: import all necessary components:
import smtplib
from socket import gaierror


driver = webdriver.Safari()

# driver.get("https://www.sreality.cz/hledani/prodej/byty/brno?stari=mesic")
driver.get(
    "https://www.sreality.cz/hledani/prodej/byty/praha-7?velikost=2%2Bkk,2%2B1,1%2B1,3%2Bkk&cena-od=0&cena-do=7000000&bez-aukce=1")
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

i = 0
for title in soup.select(".text-wrap"):
    i = i + 1
    num = "https://www.sreality.cz" + title.select_one(".title").get('href')
    print(num)

print(i)
print()


# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com:587')
s.ehlo()

# start TLS for security
s.starttls()

# Authentication
s.login("michalmandlik@gmail.com", "b626b626")

# message to be sent
message = str(i)  #'Message_you_need_to_send'

# sending the mail
s.sendmail("michalmandlik@gmail.com", "michalmandlik@gmail.com", message)

# terminating the session
s.quit()