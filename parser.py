from selenium.webdriver.common.by import By


def parse(products):
    return [parseProduct(product) for product in products]


def parseProduct(product):
    productObj = {}

    productObj['title'] = product.find_element(
        By.CLASS_NAME, 'product-description__title').get_attribute('innerHTML')

    return productObj

    # Title
    # Image
    # Price (from)
    # Price (to)
