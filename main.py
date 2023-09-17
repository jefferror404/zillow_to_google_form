import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import lxml
import time

#Input the URL of your target search on Zillow
ZILLOW_URL = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-122.58610812548828%2C%22east%22%3A-122.28055087451172%2C%22south%22%3A37.67413794910111%2C%22north%22%3A37.876307747101116%7D%2C%22mapZoom%22%3A12%2C%22usersSearchTerm%22%3A%22San%20Francisco%20CA%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22price%22%3A%7B%22max%22%3A562687%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%7D"
#Input the google form link URL that you created for inputting the search results
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLScDjvYTQYsBi4qRlz8Rz2Cd7Yieotj7F_dv606jw7Y3KNQw0g/viewform?usp=sf_link"

headers = {
    "User-Agent": "Your user agent",
    "Accept": "Your accept",
    "authority": "https://www.zillow.com/",
    "pragma": "no-cache",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "Accept-Language": "Your accept language",
}

response = requests.get(url=ZILLOW_URL, headers=headers)
zillow_site = response.text

soup = BeautifulSoup(zillow_site, "lxml")

#Get all the links from the search results
all_link_elements = soup.find_all("a", class_="StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jnnxAW property-card-link")
all_links = []
for link in all_link_elements:
    href = link["href"]
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

#Get all the addresses from the search results
all_addresses_elements = soup.find_all("address")
all_addresses = []
for address in all_addresses_elements:
    address = address.getText().split(" | ")[-1]
    all_addresses.append(address)

#Get all the prices from the search results
all_prices_elements = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr")
all_prices = []
for price in all_prices_elements:
    price = price.getText()
    all_prices.append(price)

# print(all_links)
# print(all_addresses)
# print(all_prices)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

#Fill in the google form
for n in range(len(all_links)):
    driver.get(GOOGLE_FORM)
    time.sleep(3)
    address = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(all_addresses[n])
    price = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(all_prices[n])
    link = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(all_links[n])
    submit = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()
driver.quit()


