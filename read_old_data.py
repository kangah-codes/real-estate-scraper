import ast
from difflib import SequenceMatcher
import random

class Item:
    def __init__(self, parent):
        self.nodes = []
        self.parent = parent
        self.has_nodes = False

    def add_node(self, node):
        if self.has_nodes:
            self.nodes.append(node)

    def remove_nodes(self, node):
        del(self.nodes)

    def __repr__(self):
        try:
            return f"{self.parent} {self.nodes}"
        except:
            return f"{self.parent}"

stack = []

with open('data.txt', 'r') as file:
    with open('towns.csv') as towns:
        towns_data = towns.readlines()
        data = file.readlines()
        with open('dat.txt','w+', encoding='utf-8') as new_data:
            regions = [
        		["Greater Accra", 1],
        		["Volta", 2],
        		["Central", 3],
        		["Western", 4],
        		["Ashanti", 5],
        		["Upper West", 6],
        		["Upper East", 7],
        		["Northern", 8],
        		["Eastern Region", 9],
        		["Brong Ahafo", 10]
        	]
            for town_line in towns_data:
                split = town_line.split(',')
                town = split[0]
                count = 0
                for line in data:
                    if SequenceMatcher(None, town, line).ratio() >= 0.6:
                        stack.append(Item([split[1], split[3], split[4]]))
                        stack[-1].has_nodes = True

                        if stack[-1].has_nodes:
                            if data[data.index(line)+1] not in stack[-1].nodes and data[data.index(line)+2] not in stack[-1].nodes:
                                stack[-1].add_node(data[data.index(line)+1].split('\n')[0])
                                stack[-1].add_node(data[data.index(line)+2].split('\n')[0])

                        for region in regions:
                            #print(stack)
                            if stack[-1].parent[0] in region[0]:
                                #print(i.nodes)
                                try:
                                    dats = stack[-1].nodes[1].split(',')
                                    price = stack[-1].nodes[0]
                                    price = price.replace(',','')
                                    #print(i.parent)

                                    new_data.write(f"{region[1]},{dats[1]},{dats[1]},{float(price)},{stack[-1].parent[1]},{stack[-1].parent[2]}\n")
                                    print(f"Wrote stack item {stack[-1]} to file")
                                except:
                                    pass
                    else:
                        pass
        new_data.close()
    towns.close()
file.close()

"""
region,area,number_bedrooms,number_bathrooms,asking_price,lat,lon
"""

# with open('new_dat.csv', 'w+') as file:
#     regions = [
# 		["Greater Accra", 1],
# 		["Volta", 2],
# 		["Central", 3],
# 		["Western", 4],
# 		["Ashanti", 5],
# 		["Upper West", 6],
# 		["Upper East", 7],
# 		["Northern", 8],
# 		["Eastern Region", 9],
# 		["Brong Ahafo", 10]
# 	]
#     for i in stack:
#         for region in regions:
#             if i.parent[0] in region[0]:
#                 #print(i.nodes)
#                 try:
#                     dats = i.nodes[1].split(',')
#                     price = i.nodes[0]
#                     price = price.replace(',','')
#                     #print(i.parent)
#                     file.write(f"{region[1]},{random.randrange(50, 700)},{int(dats[1])},{int(dats[1])},{float(price)},{i.parent[1]},{i.parent[2]}\n")
#                 except:
#                     pass
#     file.close()
