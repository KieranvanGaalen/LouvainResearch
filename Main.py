import matplotlib.pyplot as pp
import networkx as nx

fastGNPNetwork = nx.fast_gnp_random_graph(100, 0.05)

print(fastGNPNetwork.degree[0])

nx.draw(fastGNPNetwork, node_color=['blue'] + ['red'] * (99), with_labels=True)

pp.show()
