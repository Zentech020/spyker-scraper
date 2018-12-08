from scraper import Scraper

supermarkets = ['ah', 'jumbo']

for supermarket in supermarkets:
    scraper = Scraper(supermarket)
    scraper.start()
    scraper.export()
    scraper.quit()
