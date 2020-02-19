import requests
from bs4 import BeautifulSoup

"""
we're going to be scraping data from sites
1. meqasa
2. jiji ghana

max for meqasa is 1026
"""

class MeqasaScraper():
    def __init__(self):
        self.site = "https://meqasa.com/apartments-for-rent-in-ghana"
        self.max_links = 1026
        self.page = None
        self.data = []
        self.flattened_data = []
        self.temp = []
        self.li_temp = []

    def scrape_meqasa_urls(self):
        for i in range(1, self.max_links):
            self.page = requests.get(self.site+f"?w={i}")
            soup = BeautifulSoup(self.page.content, 'html.parser')

            pages = soup.find_all('div', class_="mqs-prop-dt-wrapper")

            for item in pages:
                current_item = BeautifulSoup(str(item), 'html.parser')

                prices = current_item.find_all('h2')
                other_data = current_item.find_all('li')
                other_flattened_data = []
                for i in other_data:
                    other_flattened_data.append(i)

                self.data.append([prices, other_flattened_data])

        for _ in self.data:
            for i in zip(_[0], f"{_[1]}"):
                item = BeautifulSoup(str(i[0]), 'html.parser')
                header = item.find('a').getText()
                self.flattened_data.append([header, _[1]])


    def write_data(self, filename, iterable):
        with open(filename, 'w+') as file:
            for line in iterable:
                file.write(str(line))
                file.write('\n')







#property = soup.find_all('div', class_='one-featured-prop')

#print(property)
a = MeqasaScraper()
a.scrape_meqasa_urls()
a.write_data('data.txt', a.flattened_data)

#print(a.flattened_data)
