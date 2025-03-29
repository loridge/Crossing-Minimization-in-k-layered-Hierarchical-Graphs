import random
import itertools
import networkx as nx
import matplotlib.pyplot as plt

def generate_k_layered_sparse_graph(k, n, m):
    """
    Generates a k-layered sparse directed graph with alternating n-m vertices per layer.

    Parameters:
    - k: Number of layers.
    - n: Number of vertices in odd layers.
    - m: Number of vertices in even layers.

    Returns:
    - nodes: List of all nodes.
    - edges: List of edges formatted as [{'nodes': ['u1', 'u4']}]
    - G: The generated k-layered directed graph.
    - layers: A list of sets, where each set contains nodes for that layer.
    """
    G = nx.DiGraph()
    layers = []
    
    # Step 1: Create layers
    vertex_counter = 1  # Start vertex count at 1
    for i in range(k):
        size = n if i % 2 == 0 else m
        layer_nodes = set(range(vertex_counter, vertex_counter + size))
        vertex_counter += size
        layers.append(layer_nodes)
        G.add_nodes_from(layer_nodes, layer=i+1)

    # Step 2: Connect adjacent layers using sparse bipartite connections
    edges = set()
    for i in range(k - 1):
        V_i = list(layers[i])
        V_next = list(layers[i + 1])
        num_edges = 2 * min(len(V_i), len(V_next))  # Sparse edge condition

        # Track edges per layer connection separately
        current_edges = set()
        
        while len(current_edges) < num_edges:
            u = random.choice(V_i)
            v = random.choice(V_next)
            if (u, v) not in edges:
                edges.add((u, v))
                current_edges.add((u, v))
                G.add_edge(u, v)

    # Convert edges to required format
    formatted_edges = [{'nodes': [f'u{u}', f'u{v}']} for u, v in edges]
    nodes = list(set.union(*layers))  # Combine all layers into one node list

    return nodes, formatted_edges, G, layers

def visualize_k_layered_graph(G, layers, title):
    """
    Visualizes a k-layered directed graph with distinct vertical layers,
    similar to the bipartite visualization style.
    
    Parameters:
    - G: The generated k-layered directed graph.
    - layers: A list of sets, where each set contains nodes for that layer.
    """
    pos = {}
    layer_gap = 2  # Vertical spacing between layers
    node_gap = 1.5  # Horizontal spacing within layers

    # Assign positions for each node
    for i, layer in enumerate(layers):
        x_offset = -len(layer) / 2  # Center nodes in each layer
        # for j, node in enumerate(sorted(layer)):  # Sorting for consistency
        for j, node in enumerate(layer): # unsorted to show real ordering
            pos[node] = (x_offset + j * node_gap, -i * layer_gap)

    # Generate pastel colors for each layer
    pastel_colors = itertools.cycle(["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#D7BAFF", "#FFC0CB"])
    layer_colors = {i: next(pastel_colors) for i in range(len(layers))}
    node_colors = [layer_colors[i] for i, layer in enumerate(layers) for node in layer]

    # Draw the graph with enhanced aesthetics
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.6, width=1.5, arrows=True)
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=node_colors, edgecolors="black")
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

    # Draw layer separators
    for i in range(len(layers)):
        plt.axhline(-i * layer_gap, color='gray', linestyle='dotted', alpha=0.5)

    # Display the graph
    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    # Example usage:
    k = 6  # Number of layers
    n = 5  # Number of vertices in odd layers
    m = 3  # Number of vertices in even layers

    nodes, formatted_edges, G, layers = generate_k_layered_sparse_graph(k, n, m)
    visualize_k_layered_graph(G, layers, "K-Layered Sparse Graph")
