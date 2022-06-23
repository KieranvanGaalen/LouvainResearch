import copy
import networkx as nx
from typing import List, Dict
from MeasureInterface import MeasureInterface

class Measure(MeasureInterface):
    def getTotalMeasure(self, G : nx.Graph, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        total = 0
        for nodesInCommunity in communitiesToNodes.values():
            total += self.getMax(G, nodesInCommunity)
        return total


    def getDelta(self, G : nx.Graph, node : int, newCommunity : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        nodesNewCommunity = copy.deepcopy(communitiesToNodes[newCommunity])
        nodesOldCommunity = copy.deepcopy(communitiesToNodes[nodesToCommunities[node]])
        oldMaxNewCommunity = self.getMax(G, nodesNewCommunity)
        oldMaxOldCommunity = self.getMax(G, nodesOldCommunity)
        newMaxNewCommunity = self.getMax(G, nodesNewCommunity.append(node))
        newMaxOldCommunity = self.getMax(G, nodesOldCommunity.remove(node))
        return (newMaxNewCommunity - oldMaxNewCommunity) + (newMaxOldCommunity - oldMaxOldCommunity)
    
    def getMax(self, G : nx.Graph, communityNodes : List[int]) -> float :
        max = 0
        for i in communityNodes:
            neighbours = G.neighbors(i)
            inCommunity = 0
            for j in neighbours:
                if j in communityNodes:
                    inCommunity += 1
            fraction = inCommunity / G.degree(i)
            if fraction > max:
                max = fraction
        return max