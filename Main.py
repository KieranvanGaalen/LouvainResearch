import matplotlib.pyplot as pp
import networkx as nx
import math
from Louvain import *

n = 100

fastGNPNetwork = nx.fast_gnp_random_graph(n, 0.01)
print(louvain_getCommunities(fastGNPNetwork))
