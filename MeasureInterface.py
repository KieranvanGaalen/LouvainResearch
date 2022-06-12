import networkx as nx
from typing import List, Dict

class MeasureInterface:
    threshold = 0

    def __init__(self): 
        pass

    def getDelta(self, G : nx.Graph, node : int, newCommunity : int, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        pass

    def getTotalMeasure(self, G : nx.Graph, communitiesToNodes : Dict[int, List[int]], nodesToCommunities : Dict[int, int]) -> float :
        pass