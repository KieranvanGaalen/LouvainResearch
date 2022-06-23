import copy
import networkx as nx
from typing import List, Dict
from MeasureInterface import MeasureInterface

class Measure(MeasureInterface):
    # Get the actual measure
    def getTotalMeasure(self, G : nx.Graph, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        total = 0
        for nodesInCommunity in communitiesToNodes.values():
            total += self.getAverage(G, nodesInCommunity)
        return total

    # Get measure difference when node is moved
    def getDelta(self, G : nx.Graph, node : int, newCommunity : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        nodesNewCommunity = copy.deepcopy(communitiesToNodes[newCommunity])
        nodesOldCommunity = copy.deepcopy(communitiesToNodes[nodesToCommunities[node]])
        oldAverageNewCommunity = self.getAverage(G, nodesNewCommunity)
        oldAverageOldCommunity = self.getAverage(G, nodesOldCommunity)
        nodesNewCommunity.append(node)
        nodesOldCommunity.remove(node)
        newAverageNewCommunity = self.getAverage(G, nodesNewCommunity)
        newAverageOldCommunity = self.getAverage(G, nodesOldCommunity)
        return (newAverageNewCommunity - oldAverageNewCommunity) + (newAverageOldCommunity - oldAverageOldCommunity)
    
    def getAverage(self, G : nx.Graph, communityNodes : List[int]) -> float :
        total = 0
        if communityNodes:
            for i in communityNodes:
                neighbours = G.neighbors(i)
                inCommunity = 0
                for j in neighbours:
                    if j in communityNodes:
                        inCommunity += 1
                total += inCommunity / G.degree(i)
            return total / len(communityNodes)
        else:
            return 0