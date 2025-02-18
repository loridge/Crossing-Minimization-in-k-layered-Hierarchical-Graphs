import random
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product

def generator_bip_graph(layer1_size, layer2_size, edge_density):
    """
    Generates a bipartite graph with a given number of nodes in each layer and a specified edge density.
    
    Parameters:
    - layer1_size (int): Number of nodes in the first layer.
    - layer2_size (int): Number of nodes in the second layer.
    - edge_density (float): Fraction of possible edges to include (0 to 1).
    
    Returns:
    - tuple: A 5-tuple containing:
        1. List of nodes in the same format as before.
        2. List of edges in the same format as before.
        3. A networkx graph object.
        4. A set of top-layer nodes.
        5. A set of bottom-layer nodes.
    """
    nodes = []
    edges = []
    G = nx.Graph()
    
    # Create nodes with depth values
    layer1 = [f"u{i+1}" for i in range(layer1_size)]
    layer2 = [f"u{i+1+layer1_size}" for i in range(layer2_size)]
    
    # Assign depths (0 for one layer, 1 for the other)
    for node in layer1:
        nodes.append({"id": node, "depth": 0})
        G.add_node(node, bipartite=0)
    for node in layer2:
        nodes.append({"id": node, "depth": 1})
        G.add_node(node, bipartite=1)
    
    # Calculate number of edges based on density
    max_edges = layer1_size * layer2_size
    num_edges = int(edge_density * max_edges)
    
    # Randomly select edges without replacement
    possible_edges = list(product(layer1, layer2))
    selected_edges = random.sample(possible_edges, min(num_edges, len(possible_edges)))
    
    for edge in selected_edges:
        edges.append({"nodes": [edge[0], edge[1]]})
        G.add_edge(edge[0], edge[1])
    
    return nodes, edges, G, set(layer1), set(layer2)

def draw_graphs_for_densities():
    layer1_size = 21
    layer2_size = 6
    densities = [i / 10 for i in range(1, 11)]  # 10%, 20%, ..., 100%
    
    fig, axes = plt.subplots(2, 5, figsize=(20, 10))
    axes = axes.flatten()
    
    for i, density in enumerate(densities):
        nodes, edges, G, top_nodes, bottom_nodes = generator_bip_graph(layer1_size, layer2_size, density)
        
        pos = {}
        pos.update((node, (i, 0)) for i, node in enumerate(top_nodes))  # Top nodes in the upper row (y=0)
        pos.update((node, (i, -1)) for i, node in enumerate(bottom_nodes))  # Bottom nodes in the lower row (y=-1)
        
        ax = axes[i]
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=700,
            node_color=['lightblue' if node in top_nodes else 'lightgreen' for node in G.nodes()],
            edge_color="gray",
            font_size=10,
            font_color="black",
            ax=ax
        )
        ax.set_title(f"Density: {int(density * 100)}%")
    
    plt.tight_layout()
    plt.show()

# Main execution logic
if __name__ == "__main__":
    draw_graphs_for_densities()