import networkx as nx
import random
from typing import List, Dict

r = random.Random(8373) # Random seed

def louvain_getCommunities(G : nx.Graph, previousTotalMeasure : float, Measure, threshold : float) -> dict : 
    nodesToCommunities = {}
    communitiesToNodes = {}
    for node in G.nodes:
        nodesToCommunities[node] = node
        communitiesToNodes[node] = [node]
    nodes = list(G.nodes)
    moved = True
    startMeasure  = Measure.getTotalMeasure(G, communitiesToNodes, nodesToCommunities)
    modNew = startMeasure
    mod = -99999999999 # Will always get into while loop
    deltaSum = 0
    if previousTotalMeasure < modNew:
        while moved and modNew - mod > threshold:
            mod = modNew
            movedCount = 0
            moved = False
            r.shuffle(nodes)
            i = 0
            for node in nodes:
                i+=1
                #prct = int(i/len(nodes)*1000)
                #if (prct % 10 == 0):
                #    print(str(int(prct/10)) + "%")
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
                    movedCount += 1
                    moved = True
            modNew = Measure.getTotalMeasure(G, communitiesToNodes, nodesToCommunities)
            print("mod delta: " + str(modNew - mod))
            print("Moved: " + str(movedCount))
            print("Communities: " + str(len(communitiesToNodes)))
        #print("deltaSum: " + str(deltaSum))
        (newNodesToCommunities, newCommunitiesToNodes) = getCommunityDicts(communitiesToNodes)
        newG = combineCommunities(G, communitiesToNodes)
        newCommunitiesToNodes = louvain_getCommunities(newG, startMeasure, Measure, threshold)
        return combineDicts(communitiesToNodes, newCommunitiesToNodes)
    else:
        return {}
    

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