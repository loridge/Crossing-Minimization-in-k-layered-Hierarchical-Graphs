"""
This module provides functions for generating, visualizing, and analyzing bipartite graphs.

Functions:
- count_crossings: Count the number of edge crossings in a bipartite graph layout.
- generate_bipartite_graph: Generate a bipartite graph with specified parameters.
- visualize_bipartite_graph: Visualize a bipartite graph with horizontal layers.
- update_positions: Update the positions of nodes for visualization after applying a heuristic.
- plot_results: Plot the experiment results, showing the number of crossings for different heuristics.
"""

import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


def count_crossings(B, pos):
    """
    Count the number of edge crossings in a bipartite graph layout.
    
    Args:
        B: The bipartite graph (NetworkX object).
        pos: A dictionary with node positions from a layout.
    
    Returns:
        Number of edge crossings in the graph.
    """
    crossings = 0
    edges = list(B.edges())
    # Iterate over all pairs of edges
    for (u1, v1), (u2, v2) in combinations(edges, 2):
        # Get positions of the edges' endpoints
        x1, x2 = pos[u1][0], pos[v1][0]
        x3, x4 = pos[u2][0], pos[v2][0]
        # Check if the edges cross (intersection in x-coordinates)
        if (x1 < x3 and x2 > x4) or (x1 > x3 and x2 < x4):
            crossings += 1
    return crossings


def generate_bipartite_graph(n1, n2, p):
    """
    Generate a bipartite graph in the specified Python format.
    
    Args:
        n1: Number of nodes in the first layer.
        n2: Number of nodes in the second layer.
        p: Probability of edge creation.
    
    Returns:
        A tuple (nodes, edges) where:
            - nodes is a list of dictionaries with "id" and "layer".
            - edges is a list of dictionaries with "nodes" as a pair of connected node IDs.
    """
    while True:
        # Create a random bipartite graph
        B = nx.bipartite.random_graph(n1, n2, p)
        print("generating")
        
        # Check if the graph is connected
        if nx.is_connected(B):
            break  # Only proceed if the graph is connected
    
    # Separate the nodes into layers
    top_nodes, bottom_nodes = nx.algorithms.bipartite.sets(B)
    
    # Create the nodes list with layer information
    nodes = []
    for node in top_nodes:
        nodes.append({"id": f"u{node}", "depth": 0})
    for node in bottom_nodes:
        nodes.append({"id": f"u{node}", "depth": 1})
    
    # Create the edges list
    edges = []
    #print("EDGES BEH" + str(B.edges()))
    for u, v in B.edges():
        edges.append({"nodes": [f"u{u}", f"u{v}"]})
    
    return nodes, edges, B, top_nodes, bottom_nodes

def visualize_bipartite_graph(B, bottom_nodes):
    """
    Visualize a bipartite graph with horizontal layers.
    
    Args:
        B: The bipartite graph (NetworkX object).
        bottom_nodes: The set of bottom_nodes nodes.
    """
    # Create a bipartite layout with horizontal orientation
    pos = nx.bipartite_layout(B, bottom_nodes, align="horizontal")
    #print("The pos is " + str(pos))
    #horizontal_pos = {node: (y, -x) for node, (x, y) in pos.items()}  # Flip x and y for horizontal layers

    # Draw the graph
    plt.figure(figsize=(10, 6))
    nx.draw(
        B,
        pos=pos,
        with_labels=True,
        node_size=700,
        node_color=['lightblue' if node in bottom_nodes else 'lightgreen' for node in B.nodes()],
        edge_color="gray",
        font_size=10,
        font_color="black",
    )
    plt.title("Bipartite Graph Visualization", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    # Calculate and display number of crossings
    crossings = count_crossings(B, pos)
    print(f"Number of edge crossings: {crossings}")


def update_positions(top_nodes, bottom_nodes):
    """
    Updates the positions of nodes for visualization after applying a heuristic.

    Args:
        top_nodes (list): The reordered list of nodes in the top layer (depth = 0).
        bottom_nodes (list): The reordered list of nodes in the bottom layer (depth = 1).

    Returns:
        dict: A dictionary of node positions in the format {node: (x, y)}.
    """
    pos = {}
    # Assign positions to top-layer nodes (y = 0 for depth 0)
    for i, node in enumerate(top_nodes):
        pos[node] = (i, 0)  # Top layer -> y = 0
    # Assign positions to bottom-layer nodes (y = 1 for depth 1)
    for i, node in enumerate(bottom_nodes):
        pos[node] = (i, 1)  # Bottom layer -> y = 1
    return pos

# Plot the results
def plot_results(df):
    """
    Plots the experiment results.
    Each combination of n1 and n2 will have its own line for each heuristic,
    using graph density instead of edge probability on the x-axis.
    """
    # Group by n1, n2 for clarity
    for n1 in df["n1"].unique():
        for n2 in df["n2"].unique():
            subset = df[(df["n1"] == n1) & (df["n2"] == n2)]
            if not subset.empty:
                plt.figure(figsize=(10, 6))
                
                # Compute graph density: Density = p
                density = subset["density"]  # In this case, density = edge probability p
                
                # X-axis: Graph density
                x = density
                
                # Y-axis: Number of crossings
                plt.plot(x, subset["crossings_original"], label="Original Layout", marker="o")
                plt.plot(x, subset["crossings_barycenter"], label="Barycenter Heuristic", marker="s")
                plt.plot(x, subset["crossings_median"], label="Median Heuristic", marker="^")
                plt.plot(x, subset["crossings_sifting"], label="Simple Sifting Heuristic", marker="x")
                # Add labels and title
                plt.title(f"Crossings for n1 = {n1}, n2 = {n2}")
                plt.xlabel("Graph Density")
                plt.ylabel("Number of Crossings")
                plt.legend()
                plt.grid(True)
                
                # Show the plot
                plt.show()
