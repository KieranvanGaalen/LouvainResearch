import networkx as nx

def louvain_getCommunities(G : nx.Graph) -> list[int] : 
    communities = []
    moved = True

    while True:
        for node in G.nodes:
            communities.append(node)
        start_mod = 0 # Calculate starting modularity here magically
        nodes = G.nodes
        while moved:
            moved = False
            nodes.shuffle()
            for node in nodes:
                best_move = -1
                best_increase = -1
                for neighbor in G.neighbors(node):
                    if communities[node] != communities[neighbor]: # Node may be moved to neighbor.
                        # Do some magic here to check if the node must be moved with heuristics
                        if True: # If may be moved placeholder.
                            best_move = communities[neighbor]
                            best_increase = 1
                if (best_increase > 0):
                    communities[node] = best_move
                    moved = True
        end_mod = 1 # Calculate final modularity placeholder
        if (end_mod < start_mod):
            break
        # Create new G and new communities list with every community being a single node
        # New community list may require rework of community list structure
    return communities