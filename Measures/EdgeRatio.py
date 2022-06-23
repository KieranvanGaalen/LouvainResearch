import networkx as nx
from typing import List, Dict
from MeasureInterface import MeasureInterface

class Measure(MeasureInterface):
    # Get the actual measure
    def getTotalMeasure(self, G : nx.Graph, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        total = 0
        for comm in communitiesToNodes:
            nodeCount = len(communitiesToNodes[comm])
            edgeCount = self.communityInnerEdgeCount(G, comm, communitiesToNodes, nodesToCommunities)
            total += edgeCount/nodeCount
        return total

    # Get measure difference when node is moved
    def getDelta(self, G : nx.Graph, node : int, newCommunity : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        oldCommunity = nodesToCommunities[node]
        oldNodeCount = len(communitiesToNodes[oldCommunity])
        newNodeCount = len(communitiesToNodes[newCommunity])
        oldEdgeCount = self.communityInnerEdgeCount(G, oldCommunity, communitiesToNodes, nodesToCommunities)
        newEdgeCount = self.communityInnerEdgeCount(G, newCommunity, communitiesToNodes, nodesToCommunities)
        oldValue = oldEdgeCount/oldNodeCount + newEdgeCount/newNodeCount
        nodeOldConnections = 0
        nodeNewConnections = 0
        for neighbour in G.neighbors(node):
            if nodesToCommunities[neighbour] == oldCommunity:
                nodeOldConnections += 1
            elif nodesToCommunities[neighbour] == newCommunity:
                nodeNewConnections += 1
        if oldNodeCount > 1:
            newValue = (oldEdgeCount - nodeOldConnections) / (oldNodeCount - 1) + (newEdgeCount + nodeNewConnections) / (oldNodeCount + 1)
        else: 
            newValue = (newEdgeCount + nodeNewConnections) / (oldNodeCount + 1) 
        return newValue - oldValue

    def communityInnerEdgeCount(self, G : nx.Graph, community : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> int :
        nodes = communitiesToNodes[community]
        edgeCount = 0

        for node in nodes:
            for neighbour in G.neighbors(node):
                 if nodesToCommunities[node] == nodesToCommunities[neighbour]:
                     edgeCount += 1
        return edgeCount / 2 # edgeCount will be counted from either side of the edge, therefore dividing by 2 should give the correct edgeCount