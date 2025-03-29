import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import os, sys
import random
import itertools
import math
import numpy as np

"""
This module provides functions for generating, visualizing, and analyzing bipartite graphs.

Functions:
- count_crossings: Count the number of edge crossings in a bipartite graph layout. <deprecated>
- generate_bipartite_graph: Generate a bipartite graph with specified parameters.
- forced_density_gen_bip_graph: for density bipartite experiments. allows singletons as of v2
- visualize_bipartite_graph: Visualize a bipartite graph with horizontal layers.
- visualize_bipartite_graph_save_file: Visualize and Save these plots
- update_positions: Update the positions of nodes for visualization after applying a heuristic.
- plot_results: Plot the experiment results, showing the number of crossings for different heuristics.
- plot_results_percentage_outliers: plotting but for percentage outliers, 
"""

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
from sifting.crossing_function import (
    cross_count_optimized,
)

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
    # print("DEBUG count_crossings function, length of edges:", len(edges))
    # print("Type of Graph:", B)
    # print("These are its combinations:", len(list(combinations(edges, 2))))
    # print("\n")
    for (u1, v1), (u2, v2) in combinations(edges, 2):
        # Get positions of the edges' endpoints
        try: 
            x1, x2 = pos[u1][0], pos[v1][0]
            x3, x4 = pos[u2][0], pos[v2][0]
        except:
            # print("DEBUG (count_crossings), edges and pos", edges, pos)
            pass
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
    # print("generating", end="")
    while True:
        # Create a random bipartite graph
        B = nx.bipartite.random_graph(n1, n2, p)
        
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

def forced_density_gen_bip_graph(n1, n2, density):
    """
    Generate a bipartite graph with a specified edge density.

    Args:
        n1 (int): Number of nodes in the first partition (layer 0).
        n2 (int): Number of nodes in the second partition (layer 1).
        density (float): Desired edge density (0 < density ≤ 1), defined as |E| / (|V1| * |V2|).

    Returns:
        tuple: (nodes, edges, B, top_nodes, bottom_nodes)
            - nodes: List of dictionaries with "id" and "depth".
            - edges: List of dictionaries with "nodes" as a pair of connected node IDs.
            - B: NetworkX bipartite graph.
            - top_nodes: Set of nodes in the first partition.
            - bottom_nodes: Set of nodes in the second partition.
    """

    # Initialize bipartite graph
    B = nx.Graph()
    top_nodes = set(range(1, n1 + 1))
    bottom_nodes = set(range(n1 + 1, n1 + n2 + 1))

    B.add_nodes_from(top_nodes, bipartite=0)
    B.add_nodes_from(bottom_nodes, bipartite=1)

    # Compute the exact number of edges required
    max_edges = n1 * n2
    num_edges = max(1, min(int(math.ceil(density * max_edges)), max_edges))  # Ensure valid range

    edges = set()

    # Step 1: Shuffle
    top_list = list(top_nodes)
    bottom_list = list(bottom_nodes)
    random.shuffle(top_list)
    random.shuffle(bottom_list)

    # note that katapat nya yung meron, 
    # for i in range(max(n1, n2)):
    #     u = top_list[i % n1]  # Cycle through top nodes
    #     v = bottom_list[i % n2]  # Cycle through bottom nodes
    #     edges.add((u, v))
    #     B.add_edge(u, v)

    # Step 2: Randomly add edges based on density (no forced connections)
    while len(edges) < num_edges:
        u = random.choice(top_list)
        v = random.choice(bottom_list)
        if (u, v) not in edges:
            edges.add((u, v))
            B.add_edge(u, v)

    # Convert to required format
    nodes = [{"id": f"u{node}", "depth": 0} for node in top_nodes] + \
            [{"id": f"u{node}", "depth": 1} for node in bottom_nodes]

    edges = [{"nodes": [f"u{u}", f"u{v}"]} for u, v in edges]
    
    return nodes, edges, B, top_nodes, bottom_nodes

def visualize_bipartite_graph(B, bottom_nodes, title):
    """
    Visualize a bipartite graph with improved aesthetics and horizontal layering.
    
    Args:
        B: The bipartite graph (NetworkX object).
        bottom_nodes: The set of bottom layer nodes.
    """
    # Generate bipartite layout with horizontal orientation
    pos = nx.bipartite_layout(B, bottom_nodes, align="horizontal")
    
    # Adjust node positions for better readability
    layer_spacing = 2  # Adjust horizontal distance
    vertical_offset = 1.5  # Adjust vertical layer spacing

    # Separate nodes into layers
    top_nodes = set(B.nodes()) - set(bottom_nodes)
    layered_pos = {node: (x * layer_spacing, y * vertical_offset) for node, (x, y) in pos.items()}

    # Generate pastel colors for each layer
    pastel_colors = itertools.cycle(["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#D7BAFF", "#FFC0CB"])
    layer_colors = {0: next(pastel_colors), 1: next(pastel_colors)}
    node_colors = [layer_colors[0] if node in top_nodes else layer_colors[1] for node in B.nodes()]

    # Draw the graph with enhanced aesthetics
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_edges(B, layered_pos, edge_color="gray", alpha=0.6, width=1.5)
    nx.draw_networkx_nodes(B, layered_pos, node_size=1500, node_color=node_colors, edgecolors="black")
    nx.draw_networkx_labels(B, layered_pos, font_size=12, font_weight="bold")

    # Display the graph
    plt.title(title, fontsize=14)
    
    ### subtitles to show crossing count
    crossings = count_crossings(B, layered_pos)
    # x_new = 
    print(f"Number of edge crossings: {crossings}")
    plt.suptitle(f"Crossings (old method): {crossings}")
    # plt.suptitle("Crossings (new method): ")
    
    
    plt.axis("off")
    plt.show()
    

    # Calculate and display number of crossings

def visualize_bipartite_graph_save_file(B, bottom_nodes, title, save_dir="graphs", filename=None):
    """
    Visualize a bipartite graph with improved aesthetics and horizontal layering, and save it to a file.
    
    Args:
        B: The bipartite graph (NetworkX object).
        bottom_nodes: The set of bottom layer nodes.
        title: The title of the graph.
        save_dir: The directory where the file should be saved (default: "graphs").
        filename: The filename to save the plot (optional). If None, a default name is generated.
    """

    # Generate bipartite layout with horizontal orientation
    pos = nx.bipartite_layout(B, bottom_nodes, align="horizontal")
    
    # Adjust node positions for better readability
    layer_spacing = 2  
    vertical_offset = 1.5  

    # Separate nodes into layers
    top_nodes = set(B.nodes()) - set(bottom_nodes)
    layered_pos = {node: (x * layer_spacing, y * vertical_offset) for node, (x, y) in pos.items()}

    # Generate pastel colors for each layer
    pastel_colors = itertools.cycle(["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#D7BAFF", "#FFC0CB"])
    layer_colors = {0: next(pastel_colors), 1: next(pastel_colors)}
    node_colors = [layer_colors[0] if node in top_nodes else layer_colors[1] for node in B.nodes()]

    # Draw the graph with enhanced aesthetics
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_edges(B, layered_pos, edge_color="gray", alpha=0.6, width=1.5)
    nx.draw_networkx_nodes(B, layered_pos, node_size=1500, node_color=node_colors, edgecolors="black")
    nx.draw_networkx_labels(B, layered_pos, font_size=12, font_weight="bold")

    # Display the graph
    plt.title(title, fontsize=14)
    
    # Compute crossings
    crossings = count_crossings(B, layered_pos)
    # newx = cross_count_optimized()
    # print(f"Number of edge crossings: {crossings}")
    plt.suptitle(f"Crossings (old method): {crossings}")
    # plt.suptitle(f"Crossings (new method): {}")
    plt.axis("off")

    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Save the figure
    if filename is None:
        filename = f"{title.replace(' ', '_')}.png"  # Default filename based on the title
    save_path = os.path.join(save_dir, filename)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Graph saved to {save_path}")

    plt.close()  # Close the plot to avoid displaying it when running in scripts
    

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


def plot_results_percentage_outliers(df, message=""):
    """
    Plots the experiment results. Also includes optional message for the title.
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
                density = subset["density"]  # In this case, density = 
                
                # X-axis: Graph density
                x = density
                
                y_barycenter = subset["avg_crossings_barycenter"] / subset["avg_crossings_optimal"] * 100
                y_median = subset["avg_crossings_median"] / subset["avg_crossings_optimal"] * 100
                y_sifting = subset["avg_crossings_sifting"] / subset["avg_crossings_optimal"] * 100
                y_optimal = subset["avg_crossings_optimal"] / subset["avg_crossings_optimal"] * 100
                
                y_barycenter = np.where(
                    subset["avg_crossings_optimal"] == 0, 
                    (subset["avg_crossings_barycenter"] + 1) / 1 * 100,  # Avoid zero division
                    (subset["avg_crossings_barycenter"] / subset["avg_crossings_optimal"]) * 100
                )
                y_median = np.where(
                    subset["avg_crossings_optimal"] == 0, 
                    (subset["avg_crossings_median"] + 1) / 1 * 100,  # Avoid zero division
                    (subset["avg_crossings_median"] / subset["avg_crossings_optimal"]) * 100
                )
                y_sifting = np.where(
                    subset["avg_crossings_optimal"] == 0, 
                    (subset["avg_crossings_sifting"] + 1) / 1 * 100,  # Avoid zero division
                    (subset["avg_crossings_sifting"] / subset["avg_crossings_optimal"]) * 100
                )
                y_optimal = np.where(
                    subset["avg_crossings_optimal"] == 0, 
                    (subset["avg_crossings_optimal"] + 1) / 1 * 100,  # Avoid zero division
                    (subset["avg_crossings_optimal"] / subset["avg_crossings_optimal"]) * 100
                )
                
                # print(y_barycenter)
                # print(y_median)
                # print(y_sifting)
                # print(y_optimal)
                # Find min and max y-values
                y_min = max(100, min(y_barycenter.min(), y_median.min(), y_sifting.min(), y_optimal.min()))
                y_max = max(y_barycenter.max(), y_median.max(), y_sifting.max(), y_optimal.max())
            
                # Round min/max to nearest 0.5
                y_min = np.floor(y_min * 2) / 2
                y_max = np.ceil(y_max * 2) / 2

                # Ensure there is at least a 0.5 difference
                if y_max - y_min < 0.5:
                    y_max = y_min + 0.5
                # Set y-axis ticks with 0.5 increments
                plt.yticks(np.arange(y_min, y_max + 0.5, 0.5))
                
                # Y-axis: Number of crossings
                # plt.plot(x, subset["avg_crossings_original"], label="Original Layout", marker="o")
                plt.plot(x,  y_barycenter, label="Barycenter Heuristic", marker="s")
                plt.plot(x, y_median, label="Median Heuristic", marker="^")
                plt.plot(x, y_sifting, label="Sifting Heuristic", marker="x")
                plt.plot(x, y_optimal, label="Optimal (Brute Force)", marker="x")
                plt.yscale('log')
                # Add labels and title
                plt.title(f"Crossings for n1 = {n1}, n2 = {n2}, {message}")
                plt.xlabel("Graph Density")
                plt.ylabel("In percentage of the minimum number of crossings")
                plt.legend()
                plt.grid(True)
                
                # Save result
                plt.savefig(f"exp3_results_{n1}+{n2}.png")
                
                # Show the plot
                plt.show()