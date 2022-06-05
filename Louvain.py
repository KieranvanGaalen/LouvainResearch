import networkx as nx
import random
from typing import List, Dict

def louvain_getCommunities(G : nx.Graph, nodesToCommunities : Dict[int, int] = {}, communitiesToNodes : Dict[int, List[int]] = {}) -> dict : 
    for node in G.nodes:
        nodesToCommunities[node] = node
        communitiesToNodes[node] = [node]
    start_mod = 0 # Calculate starting modularity here magically
    nodes = list(G.nodes)
    everMoved = False
    moved = True
    while moved:
        moved = False
        random.shuffle(nodes)
        for node in nodes:
            best_move = 0
            best_increase = 0
            for neighbour in G.neighbors(node):
                neighbourcomm = nodesToCommunities[neighbour]
                if nodesToCommunities[node] != neighbourcomm: # Node may be moved to neighbor.
                    delta = getDelta(G, node, neighbourcomm, communitiesToNodes, nodesToCommunities)
                    if delta > best_increase: # If may be moved placeholder.
                        best_move = nodesToCommunities[neighbour]
                        best_increase = delta
            if (best_increase > 0):
                communitiesToNodes[nodesToCommunities[node]].remove(node)
                if len(communitiesToNodes[nodesToCommunities[node]]) == 0:
                    communitiesToNodes.pop(nodesToCommunities[node], None)
                communitiesToNodes[best_move].append(node)
                nodesToCommunities[node] = best_move
                moved = True
                everMoved = True
    end_mod = 1 # Calculate final modularity placeholder
    return communitiesToNodes
    if (not everMoved):
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

def getDelta(G : nx.Graph, node : int, newCommunity : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
    communityInnerEdgeCount = CommunityInnerEdgeCount(G, newCommunity, communitiesToNodes, nodesToCommunities)
    communityOuterEdgeCount = CommunityOuterEdgeCount(G, newCommunity, communitiesToNodes, nodesToCommunities)
    nodeInnerEdgeCount = NodeInnerEdgeCount(G, node, newCommunity, communitiesToNodes, nodesToCommunities)
    nodeOuterEdgeCount = NodeOuterEdgeCount(G, node, newCommunity, communitiesToNodes, nodesToCommunities)

    return nodeInnerEdgeCount - (((communityInnerEdgeCount + communityOuterEdgeCount) * (nodeInnerEdgeCount + nodeOuterEdgeCount)) / (2 * len(G.edges)))

def CommunityInnerEdgeCount(G : nx.Graph, community : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> int :
    nodes = communitiesToNodes[community]
    edgeCount = 0

    for node in nodes:
        for neighbour in G.neighbors(node):
             if nodesToCommunities[node] == nodesToCommunities[neighbour]:
                 edgeCount += 1
    return edgeCount / 2 # edgeCount will be counted from either side of the edge, therefore dividing by 2 should give the correct edgeCount

def CommunityOuterEdgeCount(G : nx.Graph, community : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> int :
    nodes = communitiesToNodes[community]
    edgeCount = 0

    for node in nodes:
        for neighbour in G.neighbors(node):
            if nodesToCommunities[node] != nodesToCommunities[neighbour]:
                edgeCount += 1
    return edgeCount 

def NodeInnerEdgeCount(G : nx.Graph, node : int, community : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> int :
    edgeCount = 0

    for neighbour in G.neighbors(node):
        if nodesToCommunities[neighbour] == community:
            edgeCount += 1
    return edgeCount

def NodeOuterEdgeCount(G : nx.Graph, node : int, community : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> int :
    edgeCount = 0

    for neighbour in G.neighbors(node):
        if nodesToCommunities[neighbour] != community:
            edgeCount += 1
    return edgeCount
