import matplotlib.pyplot as pp
import networkx as nx

fastGNPNetwork = nx.fast_gnp_random_graph(100, 0.05)
information = nx.path_graph(10)

print(information.degree[0])

nx.draw(fastGNPNetwork, node_color=['blue','red'], with_labels=True)

pp.show()
