import requests
from bs4 import BeautifulSoup
import json
from difflib import SequenceMatcher


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

class JumiaScraper:
    def __init__(self):
        self.site = "https://deals.jumia.com.gh/studio-room-for-rent?page="
        self.max_links = 4
        self.page = None
        self.data = []
        self.flattened_data = []
        self.temp = []
        self.li_temp = []
        self.keys = []

    def scrape(self):
        with open ('jumia_data.txt', 'w+') as file:
            for i in range(1, self.max_links):
                self.page = requests.get(self.site+f"{i}")
                soup = BeautifulSoup(self.page.content, 'html.parser')

                pages = soup.findAll(attrs={"id" : "search-results"})
                #print(pages)

                for i in json.loads(pages[0]['data-catalog-event'])['impressions']:
                    file.write(f"{i['name']},{i['price']}\n")
        file.close()

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
        for i in range(1, 3):
            self.page = requests.get(self.site+f"{i}")
            soup = BeautifulSoup(self.page.content, 'html.parser')

            pages = soup.find_all(attrs={"data-testid":"ad-meta"})

            print(pages[0])

class JijiScraper:
    def __init__(self):
        self.site = "https://jiji.com.gh/houses-apartments-for-rent"
        self.page = None

    def scrape(self):
        self.page = requests.get(self.site)
        soup = BeautifulSoup(self.page.content, 'html.parser')

        items = soup.find_all('div', categoryslug_="houses-apartments-for-rent")
        print(items)

        for i in items:
            print(i)
            current = BeautifulSoup(str(i), 'html.parser')
            name = current.find_all('div', class_="b-advert-title-inner")
            price = current.find_all('div', class_="qa-advert-price")
            specs = current.find_all('div', class_="b-list-advert__item-attr")
            location = current.find_all('svg', class_="region")

            print(name.text, price.text, specs, location.text)

stack = []

class LocantoScraper:
    def __init__(self):
        self.site = "https://accra.locanto.com.gh/Flats-for-Rent/301/"
        self.max_links = 5
        self.page = None
        self.data = []
        self.flattened_data = []
        self.temp = []
        self.li_temp = []
        self.keys = ['title', 'details', 'price', 'location']

    def scrape(self):
        with open('locanto.txt', 'w+', encoding='utf-8') as file:
            for i in range(1, self.max_links):
                self.page = requests.get(self.site+f"{i}/")
                soup = BeautifulSoup(self.page.content, 'html.parser')

                pages = soup.find_all('div', class_="resultMain")

                for i in pages:
                    #print(f"At {i}\n")
                    #for town_line in towns_data:
                    # print(f"At {town_line}\n")
                    # split = town_line.split(',')
                    current = BeautifulSoup(str(i), 'html.parser')
                    name = current.find_all('a', class_="bp_ad__title_link")
                    loc = current.find_all('div', class_="bp_ad__city")
                    price = current.find_all('div', class_="bp_ad__price")

                    for item in zip(name, loc, price):
                        a = f"1,{item[0].text},{item[1].text},{item[2].text.replace('GH₵','')}\n"
                        file.write(a)
                        print(a)

        file.close()
a = JijiScraper()
a.scrape()

# a = LocantoScraper()
# a.scrape()
#property = soup.find_all('div', class_='one-featured-prop')
# a = JumiaScraper()
# a.scrape()
# a = TonatonScraper()
# a.scrape_tonaton_urls()
#print(property)
# a = TonatonScraper()
#
# a.scrape_tonaton_urls()
# a.scrape_meqasa_urls()
# a.write_data('data.txt', a.flattened_data)

#print(a.flattened_data)

# a = TonatonScraper()
# a.scrape_tonaton_urls()
