import matplotlib.pyplot as pp
import networkx as nx
import math
from Louvain import *

n = 100

k = {0 : [1,2,3], 1 : [0,2,3], 2 : [0,1,3], 3 : [0,1,2,5,9], 4: [5,6,7], 5 : [3,4,6,7,12], 6: [4,5,7], 7 : [4,5,6], 8 : [9,10,11], 9 : [8,10,11,3,12], 10 : [8,9,11], 11: [8,9,10], 12:[5,9,13,14,15], 13: [12,14,15], 14: [12,13,15], 15 : [12,14,13]}
graph = nx.from_dict_of_lists(k)
fastGNPNetwork = nx.barbell_graph(50, 0)
commDict = louvain_getCommunities(fastGNPNetwork.copy())

print(commDict)

nx.draw(fastGNPNetwork, node_color=['blue'] + ['red'] * (99), with_labels=True)

pp.show()
