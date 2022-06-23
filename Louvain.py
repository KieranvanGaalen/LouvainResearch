import networkx as nx
import random
from typing import List, Dict

r = random.Random(8373) # Random seed

# Runs Louvain on a graph.
def louvain_getCommunities(G : nx.Graph, previousTotalMeasure : float, Measure, threshold : float) -> dict : 
    nodesToCommunities = {}
    communitiesToNodes = {}
    # Create community for every node
    for node in G.nodes:
        nodesToCommunities[node] = node
        communitiesToNodes[node] = [node]
    nodes = list(G.nodes)
    moved = True
    # Calculate measure before moves
    startMeasure  = Measure.getTotalMeasure(G, communitiesToNodes, nodesToCommunities)
    modNew = startMeasure
    mod = -99999999999 # Will always get into while loop
    deltaSum = 0
    if previousTotalMeasure < modNew:
        while moved and modNew - mod > threshold:
            mod = modNew
            movedCount = 0
            moved = False
            # Randomise nodes (fixed seed)
            r.shuffle(nodes)
            for node in nodes:
                best_move = 0
                best_increase = 0
                # Evaluate all possible neighbours
                for neighbour in G.neighbors(node):
                    neighbourcomm = nodesToCommunities[neighbour]
                    if nodesToCommunities[node] != neighbourcomm: # Node may be moved to neighbor (not in same community).
                        delta = Measure.getDelta(G, node, neighbourcomm, communitiesToNodes, nodesToCommunities)
                        if delta > best_increase:
                            best_move = nodesToCommunities[neighbour]
                            best_increase = delta
                if (best_increase > 0):
                    deltaSum += best_increase
                    communitiesToNodes[nodesToCommunities[node]].remove(node) # Remove node from old community
                    if len(communitiesToNodes[nodesToCommunities[node]]) == 0: # If the community is empty, remove it.
                        communitiesToNodes.pop(nodesToCommunities[node], None)
                    communitiesToNodes[best_move].append(node) # Add node to new community
                    nodesToCommunities[node] = best_move
                    movedCount += 1
                    moved = True
            modNew = Measure.getTotalMeasure(G, communitiesToNodes, nodesToCommunities)
            print("mod delta: " + str(modNew - mod))
            print("Moved: " + str(movedCount))
            print("Communities: " + str(len(communitiesToNodes)))
        newG = combineCommunities(G, communitiesToNodes)
        newCommunitiesToNodes = louvain_getCommunities(newG, startMeasure, Measure, threshold)
        return combineDicts(communitiesToNodes, newCommunitiesToNodes)
    else:
        return {}
    
# Combines the community to nodes dictionaries from two different iterations into one.
def combineDicts(commToNodes : dict, newCommToNodes) -> dict :
    if (newCommToNodes == {}):
        return commToNodes
    for comm in newCommToNodes:
        newNodes = []
        for node in newCommToNodes[comm]:
            newNodes.extend(commToNodes[node])
        newCommToNodes[comm] = newNodes
    return newCommToNodes

# Create a new graph where each community is one node.
def combineCommunities(G : nx.Graph, communities : Dict[int, List[int]])  ->  nx.Graph :
    newGraph = G
    renameDict = {}
    for comm in communities:
        nodes = communities[comm]
        for i in range(1,len(nodes)):
            newGraph = nx.contracted_nodes(newGraph, nodes[0], nodes[i], False, False)
        renameDict[nodes[0]] = comm
    return nx.relabel_nodes(newGraph, renameDict, False)