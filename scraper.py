from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import parser

driver = webdriver.Chrome('/Users/roybroertjes/Desktop/scraper/chromedriver')

# load URL
url = 'https://www.ah.nl/bonus'
driver.get(url)

# Wait till bonus is rendered
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product")))
finally:
    products = driver.find_elements(By.CLASS_NAME, 'product')

productsParsed = parser.parse(products)
for product in productsParsed:
    print product
