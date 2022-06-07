import networkx as nx
import random
from typing import List, Dict

def louvain_getCommunities(G : nx.Graph, Measure, nodesToCommunities : Dict[int, int] = {}, communitiesToNodes : Dict[int, List[int]] = {}) -> dict : 
    for node in G.nodes:
        nodesToCommunities[node] = node
        communitiesToNodes[node] = [node]
    nodes = list(G.nodes)
    moved = True
    totalMeasure = Measure.getTotalMeasure(G, communitiesToNodes, nodesToCommunities)
    deltaSum = 0
    while moved:
        moved = False
        random.shuffle(nodes)
        for node in nodes:
            best_move = 0
            best_increase = 0
            for neighbour in G.neighbors(node):
                neighbourcomm = nodesToCommunities[neighbour]
                if nodesToCommunities[node] != neighbourcomm: # Node may be moved to neighbor.
                    delta = Measure.getDelta(G, node, neighbourcomm, communitiesToNodes, nodesToCommunities)
                    if delta > best_increase: # If may be moved placeholder.
                        best_move = nodesToCommunities[neighbour]
                        best_increase = delta
            if (best_increase > 0):
                deltaSum += best_increase
                communitiesToNodes[nodesToCommunities[node]].remove(node)
                if len(communitiesToNodes[nodesToCommunities[node]]) == 0:
                    communitiesToNodes.pop(nodesToCommunities[node], None)
                communitiesToNodes[best_move].append(node)
                nodesToCommunities[node] = best_move
                moved = True
    newTotalMeasure = Measure.getTotalMeasure(G, communitiesToNodes, nodesToCommunities)
    print("deltaSum: " + str(deltaSum))
    print("totalDelta: " + str(newTotalMeasure - totalMeasure))
    if (totalMeasure < newTotalMeasure):
        (newNodesToCommunities, newCommunitiesToNodes) = getCommunityDicts(communitiesToNodes)
        newG = combineCommunities(G, communitiesToNodes)
        newCommunitiesToNodes = louvain_getCommunities(newG, Measure, newNodesToCommunities, newCommunitiesToNodes)
        return combineDicts(communitiesToNodes, newCommunitiesToNodes)
    else:
        return communitiesToNodes
    

def combineDicts(commToNodes : dict, newCommToNodes) -> dict :
    if (newCommToNodes == {}):
        return commToNodes
    for comm in newCommToNodes:
        newNodes = []
        for node in newCommToNodes[comm]:
            newNodes.extend(commToNodes[node])
        newCommToNodes[comm] = newNodes
    return newCommToNodes

def getCommunityDicts(commToNodes : dict) -> tuple[dict, dict] :
    newCommToNodes = {}
    newNodesToComms = {}
    for comm in commToNodes:
        newCommToNodes[comm] = [comm]
        newNodesToComms[comm] = comm
    return (newNodesToComms, newCommToNodes)
    
def combineCommunities(G : nx.Graph, communities : Dict[int, List[int]])  ->  nx.Graph :
    newGraph = G
    renameDict = {}
    for comm in communities:
        nodes = communities[comm]
        for i in range(1,len(nodes)):
            newGraph = nx.contracted_nodes(newGraph, nodes[0], nodes[i], False, False)
        renameDict[nodes[0]] = comm
    return nx.relabel_nodes(newGraph, renameDict, False)