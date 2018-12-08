from selenium.webdriver.common.by import By

from datetime import datetime
import re

# selectors to use to find properties about a deal, such as:
#   - name, priceFrom, priceTo, description & image
selectors = {
    'name': {
        'ah': {
            'selector': '.product-description__title',
            'attribute': 'innerHTML'
        },
        'jumbo': {
            'selector': '.jum-item-titlewrap h3',
            'attribute': 'innerHTML'
        }
    },
    'priceFrom': {
        'ah': {
            'selector': '.price--was .price__text',
            'attribute': 'innerHTML'
        },
        'jumbo': {
            'selector': '.jum-promotion-price span',
            'attribute': 'innerHTML'
        }
    },
    'priceTo': {
        'ah': {
            'selector': '.price--discount span',
            'attribute': 'innerHTML'
        },
        'jumbo': {
            'selector': '.jum-promotion-price strong',
            'attribute': 'innerHTML'
        }
    },
    'description': {
        'ah': {
            'selector': '.product-description__unit-size',
            'attribute': 'innerHTML'
        },
        'jumbo': {
            'selector': '.jum-promotion-text-field:not(.jum-promotion-price)',
            'attribute': 'innerHTML'
        }
    },
    'discountTag': {
        'ah': {
            'selector': '.discount-block__label',
            'attribute': 'innerHTML'
        },
        'jumbo': {
            'selector': '.jum-mediumbadge img',
            'attribute': 'alt'
        }
    },
    # 'image': {
    #     'ah': {
    #         'selector': '.product-image-container .image-container img.product-image',
    #         'attribute': 'src'
    #     },
    #     'jumbo': {
    #         'selector': 'dd.jum-item-figure img',
    #         'attribute': 'src',
    #     }
    # }
}

# information that should be present inside a deal to make it a valid deal
requiredProperties = ['name', 'priceFrom', 'priceTo']

class Parser:
    def __init__(self, driver, supermarket):
        self.driver = driver
        self.supermarket = supermarket
        self.deals = []
        self.validUntil = ''

    def parse(self, deals):
        self.validUntil = self.__parseValidUntil()
        self.deals = [self.parseDeal(deal) for i, deal in enumerate(deals)]

    def parseDeal(self, deal):
        elements = self.__findElements(deal)

        # not all required properties are found, deal is invalid
        if not self.__validate(elements):
            return

        # get all content for each element inside deal
        return self.__getAttributes(elements)

    def printDeals(self):
        printableFields = [
            { 'key' : 'name', 'label' : 'Naam' },
            { 'key' : 'priceFrom', 'label' : 'Prijs (van)' },
            { 'key' : 'priceTo', 'label' : 'Prijs (naar)' },
            { 'key' : 'description', 'label' : 'Beschrijving' },
            { 'key' : 'discountTag', 'label' : 'Soort korting' },
            { 'key' : 'validUntil', 'label' : 'Korting loopt tot' },
            { 'key' : 'image', 'label' : 'Productfoto' }
        ]

        for deal in self.deals:
            print('\n')
            for field in printableFields:
                print field['label'], ': ', deal[field['key']]

    def __findElements(self, deal):
        elements = {}

        for property in selectors:
            selector = selectors[property][self.supermarket]['selector']

            try:
                element = deal.find_elements(By.CSS_SELECTOR, selector)
                elements[property] = element
            except:
                pass

        return elements

    def __validate(self, deal):
        for required in requiredProperties:
            if required not in deal:
                return False

        return True

    def __getAttributes(self, deal):
        for property in deal:
            attribute = ''

            for element in deal[property]:
                attribute += clean_html(element.get_attribute(selectors[property][self.supermarket]['attribute']).encode('utf-8'))

            deal[property] = attribute
            print deal['name']

        deal['supermarket'] = self.supermarket
        deal['validUntil'] = self.validUntil

        return deal

    def __parseValidUntil(self):
        switcher = {
            'ah' : self.__parseValidUntilAH,
            'jumbo' : self.__parseValidUntilJumbo
        }

        parser =  switcher.get(self.supermarket, lambda: 'Invalid supermarket!')
        validUntil = parser()

        print validUntil
        return validUntil

    def __parseValidUntilAH(self):
        return '12-07'

    def __parseValidUntilJumbo(self):
        try:
            dateString = self.driver.find_element(By.CSS_SELECTOR, '.jumbo-lister-navigation-tabs li').get_attribute('innerHTML').split()[-1]
            date = datetime.strptime(dateString + '-2018', '%d-%m-%Y')

            return date
        except:
            pass


def clean_html(html):
    cleanr = re.compile('<.*?>')

    return re.sub(cleanr, ' ', html)
