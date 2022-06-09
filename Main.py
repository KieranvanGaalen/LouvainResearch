import matplotlib.pyplot as pp
import networkx as nx
import math
from Louvain import *
from Measures import EdgeRatio, Modularity
import time

seed = 5 # TODO: Set this

n = 100

k = {0 : [1,2,3], 1 : [0,2,3], 2 : [0,1,3], 3 : [0,1,2,5,9], 4: [5,6,7], 5 : [3,4,6,7,12], 6: [4,5,7], 7 : [4,5,6], 8 : [9,10,11], 9 : [8,10,11,3,12], 10 : [8,9,11], 11: [8,9,10], 12:[5,9,13,14,15], 13: [12,14,15], 14: [12,13,15], 15 : [12,14,13]}
graph = nx.from_dict_of_lists(k)
fastGNPNetwork = nx.barbell_graph(50, 0)

runtimes = [] # Use this for runtime analysis
for _ in range(10):
    sizes = [75, 75, 300] # TODO: Randomise this based on seed
    probs = [[0.25, 0.05, 0.02], [0.05, 0.35, 0.07], [0.02, 0.07, 0.40]] # TODO: Randomise this based on seed
    stochasticGraph = nx.stochastic_block_model(sizes, probs)

    start = time.time()
    commDict = louvain_getCommunities(float('-inf'), fastGNPNetwork.copy(), Modularity.Measure())
    end = time.time()
    runtimes.append(end - start)

    #print("runtime: " + str(end - start))
    print(commDict)
    # TODO: Ground truth analysis

nx.draw(fastGNPNetwork, node_color=['blue'] + ['red'] * (99), with_labels=True)

pp.show()
