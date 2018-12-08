from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
from datetime import datetime

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
        self.parser = None

    def start(self):
        self.driver.get(self.url)

        # wait till deals are rendered by JS
        try:
            WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, products[self.supermarket])))
        finally:
            # preprocessing (for "Jumbo" trigger scroll loading for example)
            self.__preprocess()

            # find deals
            deals = self.driver.find_elements(By.CLASS_NAME, products[self.supermarket])

            # parse deals
            self.parser = Parser(self.driver, self.supermarket)
            self.parser.parse(deals)

            # print deals
            # self.parser.printDeals()

    def export(self):
        keys = ['name', 'supermarket', 'priceFrom', 'priceTo', 'description', 'discountTag', 'validUntil']
        week = str(datetime.now().isocalendar()[1])

        with open('deals/week' + week + '-' + self.supermarket + '.csv', 'wb') as output:
            DW = csv.DictWriter(output, keys)
            DW.writeheader()
            DW.writerows(self.parser.deals)

    def quit(self):
        self.driver.quit()

    def __preprocess(self):
        switcher = {
            'ah' : self.__preprocessAH,
            'jumbo' : self.__preprocessJumbo
        }

        processor = switcher.get(self.supermarket, lambda: 'Invalid supermarket!')
        processor()

    def __preprocessAH(self):
        pass

    def __preprocessJumbo(self):
        while not self.driver.find_elements_by_css_selector('.jum-infscroll-message #infscr-loading div'):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(5)
