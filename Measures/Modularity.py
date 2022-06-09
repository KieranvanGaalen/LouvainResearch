import networkx as nx
from typing import List, Dict
from MeasureInterface import MeasureInterface

class Measure(MeasureInterface):


    def getDelta(self, G : nx.Graph, node : int, newCommunity : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        communityInnerEdgeCount = self.communityInnerEdgeCount(G, newCommunity, communitiesToNodes, nodesToCommunities)
        communityOuterEdgeCount = self.communityOuterEdgeCount(G, newCommunity, communitiesToNodes, nodesToCommunities)
        nodeInnerEdgeCount = self.nodeInnerEdgeCount(G, node, newCommunity, communitiesToNodes, nodesToCommunities)
        nodeOuterEdgeCount = self.nodeOuterEdgeCount(G, node, newCommunity, communitiesToNodes, nodesToCommunities)

        return nodeInnerEdgeCount - (((communityInnerEdgeCount + communityOuterEdgeCount) * (nodeInnerEdgeCount + nodeOuterEdgeCount)) / (2 * len(G.edges)))

    def communityInnerEdgeCount(self, G : nx.Graph, community : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> int :
        nodes = communitiesToNodes[community]
        edgeCount = 0

        for node in nodes:
            for neighbour in G.neighbors(node):
                 if nodesToCommunities[node] == nodesToCommunities[neighbour]:
                     edgeCount += 1
        return edgeCount / 2 # edgeCount will be counted from either side of the edge, therefore dividing by 2 should give the correct edgeCount

    def communityOuterEdgeCount(self, G : nx.Graph, community : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> int :
        nodes = communitiesToNodes[community]
        edgeCount = 0

        for node in nodes:
            for neighbour in G.neighbors(node):
                if nodesToCommunities[node] != nodesToCommunities[neighbour]:
                    edgeCount += 1
        return edgeCount 

    def nodeInnerEdgeCount(self, G : nx.Graph, node : int, community : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> int :
        edgeCount = 0

        for neighbour in G.neighbors(node):
            if nodesToCommunities[neighbour] == community:
                edgeCount += 1
        return edgeCount

    def nodeOuterEdgeCount(self, G : nx.Graph, node : int, community : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> int :
        edgeCount = 0

        for neighbour in G.neighbors(node):
            if nodesToCommunities[neighbour] != community:
                edgeCount += 1
        return edgeCount

    def getTotalMeasure(self, G : nx.Graph, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float : #total measure is modularity here
        result = 0
        for c in communitiesToNodes:
            for i in communitiesToNodes[c]:
                for j in communitiesToNodes[c]:
                    if j in G.neighbors(i):
                        result += 1 - (sum(1 for _ in G.neighbors(i))) * (sum(1 for _ in G.neighbors(j))) / (2 * G.number_of_edges())
                    else:
                        result -= (sum(1 for _ in G.neighbors(i))) * (sum(1 for _ in G.neighbors(j))) / (2 * G.number_of_edges())
        return result / (2 * G.number_of_edges())