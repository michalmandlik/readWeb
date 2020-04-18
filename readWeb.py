from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Safari()

# driver.get("https://www.sreality.cz/hledani/prodej/byty/brno?stari=mesic")
driver.get(
    "https://www.sreality.cz/hledani/prodej/byty/praha-7?velikost=1%2B1,2%2Bkk,2%2B1,3%2Bkk&stari=mesic&cena-od=0&cena-do=7000000&bez-aukce=1")
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

i = 0
for title in soup.select(".text-wrap"):
    i = i + 1
    num = "https://www.sreality.cz" + title.select_one(".title").get('href')
    print(num)

print(i)
