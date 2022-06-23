import copy
import networkx as nx
from typing import List, Dict
from MeasureInterface import MeasureInterface

class Measure(MeasureInterface):
    # Get the actual measure
    def getTotalMeasure(self, G : nx.Graph, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        total = 0
        for nodesInCommunity in communitiesToNodes.values():
            total += self.getMin(G, nodesInCommunity)
        return total

    # Get measure difference when node is moved
    def getDelta(self, G : nx.Graph, node : int, newCommunity : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        nodesNewCommunity = copy.deepcopy(communitiesToNodes[newCommunity])
        nodesOldCommunity = copy.deepcopy(communitiesToNodes[nodesToCommunities[node]])
        oldMinNewCommunity = self.getMin(G, nodesNewCommunity)
        oldMinOldCommunity = self.getMin(G, nodesOldCommunity)
        nodesNewCommunity.append(node)
        nodesOldCommunity.remove(node)
        newMinNewCommunity = self.getMin(G, nodesNewCommunity)
        newMinOldCommunity = self.getMin(G, nodesOldCommunity)
        return (newMinNewCommunity - oldMinNewCommunity) + (newMinOldCommunity - oldMinOldCommunity)
    
    def getMin(self, G : nx.Graph, communityNodes : List[int]) -> float :
        min = float('inf')
        if communityNodes:
            for i in communityNodes:
                neighbours = G.neighbors(i)
                inCommunity = 0
                for j in neighbours:
                    if j in communityNodes:
                        inCommunity += 1
                fraction = inCommunity / G.degree(i)
                if fraction < min:
                    min = fraction
        else:
            min = 0
        return min