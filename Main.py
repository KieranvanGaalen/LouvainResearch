from uuid import getnode
import matplotlib.pyplot as pp
import networkx as nx
import math
from Louvain import *
from Measures import EdgeRatio, Modularity
import time
import os
import csv

measureToRun = EdgeRatio
seed = 15

def getCommDict(G : nx.graph) -> Dict[int, int]:
    nodeToComm = {}
    commIndex = 0
    attr = nx.get_node_attributes(G,"community")
    for node in G.nodes(data=True):
        if node[0] not in nodeToComm:
            for node2 in node[1]['community']:
                nodeToComm[node2] = commIndex
            commIndex += 1
    return nodeToComm

def getNodeToComm(commToNode : Dict[int, List[int]]) -> Dict[int, int]:
    nodeToComm = {}
    for comm in commToNode:
        for node in commToNode[comm]:
            nodeToComm[node] = comm
    return nodeToComm

def writeLists(measureToRun, runTimes : List[float], edgeCounts : List[int], nodeCounts : List[int], groundTruths : List[float]):
    dirname = os.path.dirname(__file__)
    splitMeasure = str(measureToRun).split('\\')
    correctMeasure = splitMeasure[len(splitMeasure) - 1]
    correctMeasure = correctMeasure[0:len(correctMeasure) - 5] + ".csv"
    filepath = os.path.join(dirname, str(correctMeasure))

    runIndices = [correctMeasure[0:len(correctMeasure) - 4]]
    for i in range(1, len(runTimes) + 1):
        runIndices.append(str(i))

    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerow(runIndices)
        writer.writerow(["runTimes"] + [str(x) for x in runTimes])
        writer.writerow(["edgeCounts"] + [str(x) for x in edgeCounts])
        writer.writerow(["nodeCounts"] + [str(x) for x in nodeCounts])
        writer.writerow(["groundTruths"] + [str(x) for x in groundTruths])

def calculateJaccardIndex(nodesToCommunitiesTrue : Dict[int, int], nodesToCommunitiesFromAlgorithm : Dict[int, int]) -> float :
    a01 = 0
    a10 = 0
    a11 = 0
    for key1 in nodesToCommunitiesTrue:
        for key2 in nodesToCommunitiesTrue:
            if key1 != key2:
                c1True = nodesToCommunitiesTrue[key1]
                c2True = nodesToCommunitiesTrue[key2]
                c1Algo = nodesToCommunitiesFromAlgorithm[key1]
                c2Algo = nodesToCommunitiesFromAlgorithm[key2]
                if c1True == c2True:
                    if c1Algo == c2Algo:
                        a11 += 1
                    else:
                        a10 += 1
                elif c1Algo == c2Algo:
                    a01 += 1
    return a11 / (a11 + a01 + a10)

runTimes = [] # Use this for runtime analysis
edgeCounts = []
nodeCounts = []
groundTruths = []


seed = 22
while True:
    try:
        random.seed(seed)
        for _ in range(20):
            # Create the lfr graph
            n = random.randrange(250, 2000)
            #print(n)
            tau1 = 3
            tau2 = 1.5
            mu = random.uniform(0.03, 0.75)
            average_degree = 20
            max_community = int(0.1 * n)
            max_degree = int(0.1 * n)
            lfrGraph = nx.LFR_benchmark_graph(n, tau1, tau2, mu, average_degree=average_degree, max_community=max_community, max_degree=max_degree, seed=seed)
        while True:
            print(seed)
            time.sleep(60)
    except:
        print(str(seed) + " failed")
        seed += 1

""""
    # Get the correct communities out of graph
    correctNodeToComm = getCommDict(lfrGraph)

    # Get the edge and node counts out of graph
    edgeCounts.append(lfrGraph.number_of_edges())
    nodeCounts.append(lfrGraph.number_of_nodes())

    print("Starting Louvain!")
    # Run Louvain, and time it
    start = time.time()
    commDict = louvain_getCommunities(float('-inf'), lfrGraph.copy(), measureToRun.Measure())
    end = time.time()

    # Transform resulting communities into same format as correct communities
    generatedNodeToComm = getNodeToComm(commDict)

    # Calculate the ground truth based on jaccard index
    groundTruth = calculateJaccardIndex(correctNodeToComm, generatedNodeToComm)

    # Get the groundTruth and runtime
    groundTruths.append(groundTruth)
    runTimes.append(end - start)
    
writeLists(measureToRun, runTimes, edgeCounts, nodeCounts, groundTruths)
"""