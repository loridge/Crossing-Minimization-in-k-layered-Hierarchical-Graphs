import networkx as nx
import matplotlib.pyplot as plt
import random

# Barycenter Algorithm Implementation
def barycenter(bottom_nodes, top_nodes, edges):
    print("---------------INSIDE BARYCENTER------------------")
    """
    Rearrange the bottom_nodes to minimize edge crossings using the barycenter heuristic.

    Args:
        bottom_nodes (list): List of nodes in the bottom layer.
        top_nodes (list): List of nodes in the top (fixed) layer.
        edges (list): List of edges, where each edge is a dictionary with "nodes".

    Returns:
        list: Rearranged order of bottom_nodes.
    """

    def get_neighbors(node, edges):
        """Get neighbors of a given node from the edges."""
        print("Inside get_neighbors, these are edges", edges)
        return [edge["nodes"][1] if edge["nodes"][0] == node else edge["nodes"][0]
                for edge in edges if node in edge["nodes"]]

    # Calculate barycenter values for each bottom node
    barycenters = []
    
    print(bottom_nodes, top_nodes)
    
    for bottom_node in bottom_nodes:
        neighbors = get_neighbors(bottom_node, edges)
        # Get the positions of neighbors in top_nodes
        positions = [top_nodes.index(neighbor) for neighbor in neighbors if neighbor in top_nodes]
        # Compute the barycenter (average position)
        barycenter_value = sum(positions) / len(positions) if positions else float('inf')
        barycenters.append((bottom_node, barycenter_value))

    # Sort bottom_nodes by barycenter values
    sorted_bottom_nodes = [node for node, _ in sorted(barycenters, key=lambda x: x[1])]
    print("---------------EXITING BARYCENTER------------------")
    return sorted_bottom_nodes




# Function to draw bipartite graph with horizontal layers
def draw_horizontal_bipartite(B, top_nodes, bottom_nodes, title, node_order=None):
    """
    Draws the bipartite graph with horizontal layers.
    
    Args:
        B: Bipartite graph.
        top_nodes: Nodes in the top layer (upper row).
        bottom_nodes: Nodes in the bottom layer (lower row).
        title: Title for the plot.
        node_order: Optional reordering for bottom nodes.
    """
    # Apply reordering if provided
    if node_order:
        bottom_nodes = node_order

    # Generate positions for horizontal layout
    pos = {}
    pos.update((node, (i, 0)) for i, node in enumerate(top_nodes))  # Top nodes in the upper row (y=0)
    pos.update((node, (i, -1)) for i, node in enumerate(bottom_nodes))  # Bottom nodes in the lower row (y=-1)

    # print("pos", pos)
    # Draw the graph
    plt.figure(figsize=(10, 6))
    nx.draw(
        B,
        pos,
        with_labels=True,
        node_size=700,
        node_color=['lightblue' if node in top_nodes else 'lightgreen' for node in B.nodes()],
        edge_color="gray",
        font_size=10,
        font_color="black"
    )
    plt.title(title, fontsize=14)
    plt.show()

# Add this block to prevent code from running when imported
if __name__ == "__main__":
    # Create a bipartite graph
    m, n = 5, 7  # Number of nodes in each partition
    B = nx.bipartite.random_graph(m, n, p=0.6)  # p controls edge density
    # # Get the two sets of nodes (partitions)
    top_nodes, bottom_nodes = nx.algorithms.bipartite.sets(B)
    print(top_nodes, bottom_nodes)
    # # Define edges as tuples of nodes
    edges = [(u, v) for u, v in B.edges()]
    print("edges", edges)
    # # Plot the graph before applying the barycenter algorithm
    draw_horizontal_bipartite(B, top_nodes, bottom_nodes, "Before Applying Barycenter Algorithm")

    # # Reorder the bottom layer using the barycenter algorithm
    optimized_bottom_order = barycenter(list(top_nodes), list(bottom_nodes), edges)

    # # Plot the graph after applying the barycenter algorithm
    draw_horizontal_bipartite(B, top_nodes, bottom_nodes, "After Applying Barycenter Algorithm", node_order=optimized_bottom_order)
