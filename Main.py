import matplotlib.pyplot as pp
import networkx as nx
import math
from Louvain import *
from Measures import EdgeRatio, Modularity
import time

seed = 5 # TODO: Set this

def getSizes(numcom : int) -> List[int]:
    sizes = []
    for i in range(numcom):
        sizes.append(random.randrange(1, 100))
    return sizes

def getProbs(numcom : int) -> List[List[int]]:
    probs = []
    for i in range(numcom):
        tmplist = []
        for j in range(numcom):
            tmplist.append(0)
        probs.append(tmplist)
    for i in range(numcom):
        for j in range(i, numcom):
            val = random.uniform(0,1)
            probs[i][j] = val
            probs[j][i] = val
    return probs

runtimes = [] # Use this for runtime analysis
edgeCounts = []
nodeCounts = []
foundComs = []
numcoms = []
for _ in range(10):
    numcom = random.randrange(1, 50)
    sizes = getSizes(numcom)
    probs = getProbs(numcom)
    print(numcom)
    print(sizes)
    print(probs)
    stochasticGraph = nx.stochastic_block_model(sizes, probs)

    numcoms.append(numcom)
    edgeCounts.append(stochasticGraph.number_of_edges())
    nodeCounts.append(stochasticGraph.number_of_nodes())
    start = time.time()
    commDict = louvain_getCommunities(stochasticGraph.copy(), EdgeRatio.Measure())
    end = time.time()
    runtimes.append(end - start)
    foundComs.append(len(commDict)
    # TODO: Ground truth analysis


