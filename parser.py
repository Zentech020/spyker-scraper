from selenium.webdriver.common.by import By

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
    }
}

# information that should be present inside a deal to make it a valid deal
requiredProperties = ['name', 'priceFrom', 'priceTo']

class Parser:
    def __init__(self, supermarket):
        self.supermarket = supermarket
        self.deals = []

    def parse(self, deals):
        return [self.parseDeal(deal) for i, deal in enumerate(deals)]

    def parseDeal(self, deal):
        elements = self.__findElements(deal)

        # not all required properties are found, deal is invalid
        if not self.__validate(elements):
            return

        # get all content for each element inside deal
        self.deals.append(self.__getAttributes(elements))

    def printDeals(self):
        for deal in self.deals:
            print("\n")
            print 'Naam: ', deal['name']
            print 'Prijs (van): ', deal['priceFrom']
            print 'Prijs (naar): ', deal['priceTo']
            print 'Beschrijving: ', deal['description']
            print 'Soort korting: ', deal['discountTag']

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
                attribute += element.get_attribute(selectors[property][self.supermarket]['attribute']).encode('utf-8')

            deal[property] = attribute

        return deal
