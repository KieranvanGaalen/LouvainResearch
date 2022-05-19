import networkx as nx

def louvain_getCommunities(G : nx.Graph) -> list[list[int]] : 
    communities = []
    for node in G.nodes:
        communities.append([node])
    return communities