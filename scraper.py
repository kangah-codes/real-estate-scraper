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
        for i in range(1, 2):
            self.page = requests.get(self.site+f"?w={i}")
            soup = BeautifulSoup(self.page.content, 'html.parser')

            pages = soup.find_all('div', class_="mqs-prop-dt-wrapper")

            for item in pages:
                current_item = BeautifulSoup(str(item), 'html.parser')

                prices = current_item.find_all('h2')
                other_data = current_item.find_all('li')
                prices = current_item.find_all('p', class_='h3')
                other_flattened_data = []
                for j in other_data:
                    other_flattened_data.append(j)
                for j in prices:
                    other_flattened_data.append(j)

                self.data.append([prices, other_flattened_data])
            print(f"Scraped page {i}")

        for _ in self.data:
            for i in zip(_[0], f"{_[1]}"):
                item = BeautifulSoup(str(i[0]), 'html.parser')
                try:
                    header = item.find('a').getText()
                    self.flattened_data.append([header, _[1]])
                except:
                    pass


    def write_data(self, filename, iterable):
        with open(filename, 'w+') as file:
            for line in iterable:
                file.write(str(line))
                file.write('\n')
                print("Wrote line to file")



class TonatonScraper():
    def __init__(self):
        self.site = "https://tonaton.com/en/ads/ghana/property?by_paying_member=0&sort=relevance&buy_now=0&query=rent&page="
        self.max_links = 126
        self.page = None
        self.data = []
        self.flattened_data = []
        self.temp = []
        self.li_temp = []
        self.keys = ['title', 'details', 'price', 'location']


    def scrape_tonaton_urls(self):
        for i in range(1, 2):
            self.page = requests.get(self.site+f"{i}")
            soup = BeautifulSoup(self.page.content, 'html.parser')

            pages = soup.find_all('script')
            items = soup.find_all(lambda tag:tag.name=="script")

            for j in items:
                print(j.text)
                # for line in j.splitlines():
                #     if line.split(':')[0].strip() in keys:
                #         print(line.strip())



#property = soup.find_all('div', class_='one-featured-prop')

#print(property)
a = MeqasaScraper()
a.scrape_meqasa_urls()
a.write_data('data.txt', a.flattened_data)

#print(a.flattened_data)

# a = TonatonScraper()
# a.scrape_tonaton_urls()