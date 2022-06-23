import copy
import networkx as nx
from typing import List, Dict
from MeasureInterface import MeasureInterface

class Measure(MeasureInterface):
    def getTotalMeasure(self, G : nx.Graph, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        total = 0
        for nodesInCommunity in communitiesToNodes.values():
            numerator = self.getNumerator(G, nodesInCommunity)
            total += numerator / len(nodesInCommunity)
        return total


    def getDelta(self, G : nx.Graph, node : int, newCommunity : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        nodesNewCommunity = copy.deepcopy(communitiesToNodes[newCommunity])
        nodesOldCommunity = copy.deepcopy(communitiesToNodes[nodesToCommunities[node]])
        numeratorNewCommunity = self.getNumerator(G, nodesNewCommunity)
        numeratorOldCommunity = self.getNumerator(G, nodesOldCommunity)
        nodeNecessaryInNewCommunity = 0
        nodeNecessaryInOldCommunity = 0
        amountInnerEdgesNewCommunity = 0
        amountInnerEdgesOldCommunity = 0
        for i in G.neighbors(node):
            if i in nodesNewCommunity:
                amountInnerEdgesNewCommunity += 1
            elif i in nodesOldCommunity:
                amountInnerEdgesOldCommunity += 1
        if amountInnerEdgesNewCommunity >= G.degree(node) / 2:
            nodeNecessaryInNewCommunity = 1
        if amountInnerEdgesOldCommunity >= G.degree(node) / 2:
            nodeNecessaryInOldCommunity = 1
        return ((numeratorNewCommunity + nodeNecessaryInNewCommunity) / (len(nodesNewCommunity) + 1) - (numeratorNewCommunity / len(nodesNewCommunity))) + ((numeratorOldCommunity - nodeNecessaryInOldCommunity) / (len(nodesOldCommunity) - 1) - (numeratorOldCommunity / len(nodesOldCommunity)))
    
    def getNumerator(self, G : nx.Graph, communityNodes : List[int]) -> int :
        counter = 0
        for i in communityNodes:
            neighbours = G.neighbors(i)
            edgesInCommunity = 0
            for j in neighbours:
                if j in communityNodes:
                    edgesInCommunity += 1
            if edgesInCommunity >= G.degree(i) / 2:
                counter += 1
        return counter