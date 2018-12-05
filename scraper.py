from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser import Parser

urls = {
    'ah': 'https://www.ah.nl/bonus',
    'jumbo': 'https://www.jumbo.com/aanbiedingen'
}

products = {
    'ah': 'product',
    'jumbo': 'jum-item-promotion'
}

class Scraper:
    def __init__(self, supermarket):
        self.supermarket = supermarket
        self.url = urls[supermarket]
        self.driver = webdriver.Chrome('./chromedriver')

    def start(self):
        self.driver.get(self.url)

        # wait till deals are rendered by JS
        try:
            WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, products[self.supermarket])))
        finally:
            # TODO: preprocessing (for "Jumbo" trigger scroll loading for example)

            # find deals
            deals = self.driver.find_elements(By.CLASS_NAME, products[self.supermarket])

            # parse deals
            parser = Parser(self.supermarket)
            parser.parse(deals)

            # print deals
            parser.printDeals()
