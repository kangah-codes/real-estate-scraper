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
        with open('locanto_data.txt', 'w+', encoding='utf-8') as file:
            with open('towns.csv') as towns:
                towns_data = towns.readlines()
                # for town_line in towns_data:
                #     split = town_line.split(',')
                #     town = split[0]
                #     count = 0
                #     for line in data:
                #         if SequenceMatcher(None, town, line).ratio() >= 0.6:
                #             stack.append(Item([split[1], split[3], split[4]]))
                #             stack[-1].has_nodes = True
                #             print(town, line)
                for i in range(1, self.max_links):
                    self.page = requests.get(self.site+f"{i}/")
                    soup = BeautifulSoup(self.page.content, 'html.parser')

                    pages = soup.find_all('div', class_="resultMain")

                    for i in pages:
                        for town_line in towns_data:
                            split = town_line.split(',')
                            current = BeautifulSoup(str(i), 'html.parser')
                            name = current.find_all('a', class_="bp_ad__title_link")
                            loc = current.find_all('div', class_="bp_ad__city")
                            price = current.find_all('div', class_="bp_ad__price")

                            for item in zip(name, loc, price):
                                if SequenceMatcher(None, split[0], item[0].text).ratio() >= 0.6:
                                    for i in item[0].text:
                                        try:

                                            file.write(f"1,{int(i)},{int(i)},{item[2].text.replace('GH₵','')},{split[3]},{split[4]}\n")
                                        except:
                                            pass
        file.close()


a = LocantoScraper()
a.scrape()
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
