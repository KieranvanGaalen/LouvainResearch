import networkx as nx
from typing import List, Dict

def louvain_getCommunities(G : nx.Graph, nodesToCommunities = {}, communitiesToNodes = {}) -> dict : 

    for node in G.nodes:
        nodesToCommunities[node] = node
        communitiesToNodes[node] = [node]
    start_mod = 0 # Calculate starting modularity here magically
    nodes = G.nodes
    moved = True
    while moved:
        moved = False
        nodes.shuffle()
        for node in nodes:
            best_move = -1
            best_increase = -1
            for neighbor in G.neighbors(node):
                if nodesToCommunities[node] != nodesToCommunities[neighbor]: # Node may be moved to neighbor.
                    # Do some magic here to check if the node must be moved with heuristics
                    if True: # If may be moved placeholder.
                        best_move = nodesToCommunities[neighbor]
                        best_increase = 1
            if (best_increase > 0):
                communitiesToNodes[nodesToCommunities[node]].remove(node)
                communitiesToNodes[best_move].append(node)
                nodesToCommunities[node] = best_move
                moved = True
    end_mod = 1 # Calculate final modularity placeholder
    if (end_mod < start_mod):
        return {}
    (newNodesToCommunities, newCommunitiesToNodes) = getCommunityDicts(communitiesToNodes)
    newCommunitiesToNodes = louvain_getCommunities(combineCommunities(G, communitiesToNodes), newNodesToCommunities, newCommunitiesToNodes)
    return combineDicts(communitiesToNodes, newCommunitiesToNodes)

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