import networkx as nx
from typing import List, Dict

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