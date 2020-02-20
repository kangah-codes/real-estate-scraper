import re
import json
import ast

stack = []

class Item:
    def __init__(self, parent):
        self.nodes = []
        self.parent = parent
        self.has_nodes = False

    def add_node(self, node):
        self.nodes.append(node)

    def remove_nodes(self, node):
        del(self.nodes)

    def __repr__(self):
        try:
            return f"<{self.parent}> <{self.nodes}>"
        except:
            return f"<{self.parent}>"


        #print(stack)

def stackify():
    with open('data.txt', 'r') as file:
        with open('towns.csv') as towns:
            for line in towns.readlines():
                for item in file.readlines():
                    if item != '\n':
                        if line.split(',')[0] in item:
                            split = line.split(',')
                            stack.append(Item([split[0], split[1], split[3], split[4]]))
                        else:
                            try:
                                stack[-1].add_node(item)
                            except:
                                pass

    with open('polished.txt', 'w+') as file:
        for item in stack:
            file.write(item)
        file.close()


"""
This is the format in which data is going to come
Dzorwulu-090427?y=964718212>4 bedroom house for rent at Dzorwulu, Ghana</a>

,

<span class=h3>Price:</span>GHâ‚µ13,597 <span></span>

, <li class=bed><span>4</span></li>, <li class=shower><span>3</span></li>, <li class=garage title=Garages><span>5</span></li>, <li class=area title=Area><span>320 m<sup>2</sup></span></li>, <li class=reduced sl90427 fav-icon><a data-target=#fav-modal data-toggle=modal href=><img alt=Unfavourite src=https://dve7rykno93gs.cloudfront.net/assets2/images/fav-icon.png title=Add to favourites/></a></li>,

<span class=h3>Price:</span>GHâ‚µ13,597 <span></span>

"""
# a = Item(True)
#
# a.readfile()
#
# for i in a.nodes:
#     print(i)
#     print("SPACE\n")
#print(a.nodes)

stackify()
