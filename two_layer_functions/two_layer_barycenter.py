import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations
import os, sys
import random

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
from .sifting_2 import (
    cross_count_optimized,
)
    
""" 
- parse_edges - for compatibility with the barycenter and median
- barycenter
- median
- permutation
"""

# Helper function to parse edge format
def parse_edges(edges, top_nodes, bottom_nodes):
    """
    Parse edges from the given format and map them to integers corresponding to top and bottom nodes.
    Args:
        edges (list): List of edges in the format [{'nodes': ['u0', 'u6']}, ...].
        top_nodes (list): List of top-layer node IDs (e.g., [0, 1, 2]).
        bottom_nodes (list): List of bottom-layer node IDs (e.g., [3, 4, 5, 6, 7]).
    
    Returns:
        list: List of tuples representing edges as (top_node, bottom_node).
    """
    parsed_edges = []
    for edge in edges:
        u, v = edge['nodes']
        # Convert 'uX' to integer node IDs
        u_id = int(u[1:])  # Remove 'u' and convert to integer
        v_id = int(v[1:])
        if u_id in top_nodes and v_id in bottom_nodes:
            parsed_edges.append((u_id, v_id))
        elif v_id in top_nodes and u_id in bottom_nodes:
            parsed_edges.append((v_id, u_id))
    # print("DEBUG: parsed_edges internal", parsed_edges, "vs", edges, "nodes",top_nodes, bottom_nodes)
    return parsed_edges

# Barycenter Heuristic Implementation
def barycenter(bottom_nodes, top_nodes, edges):
    # Ensure top_nodes is a list
    top_nodes = list(top_nodes)

    # Create a dictionary to store the neighbors of each bottom node
    neighbors = {node: set() for node in bottom_nodes}
    for u, v in edges:
        if u in top_nodes:
            neighbors[v].add(u)
        else:
            neighbors[u].add(v)

    # Calculate barycenter values for bottom nodes
    barycenter_values = {}
    for node in bottom_nodes:
        if len(neighbors[node]) > 0:
            barycenter_values[node] = sum(top_nodes.index(n) + 1 for n in neighbors[node]) / len(neighbors[node])
        else:
            barycenter_values[node] = float('inf')  # Assign a very high value for isolated nodes

    # Sort bottom nodes based on barycenter values
    sorted_bottom_nodes = sorted(bottom_nodes, key=lambda x: barycenter_values[x])

    return sorted_bottom_nodes

def median(bottom_nodes, top_nodes, edges):
    """
    Reorders bottom nodes using the median heuristic.
    
    Parameters:
    - bottom_nodes: List of bottom-layer nodes.
    - top_nodes: List of top-layer nodes.
    - edges: List of tuples representing edges (top_node, bottom_node).
    
    Returns:
    - Reordered list of bottom-layer nodes.
    """
    # Ensure top_nodes is a list
    top_nodes = list(top_nodes)
    # Dictionary to store neighbors of each bottom node
    neighbors = {node: [] for node in bottom_nodes}
    
    # Populate neighbors dictionary
    for u, v in edges:
        if u in top_nodes and v in bottom_nodes:
            neighbors[v].append(top_nodes.index(u) + 1)
        elif v in top_nodes and u in bottom_nodes:
            neighbors[u].append(top_nodes.index(v) + 1)
    
    # Compute the median for each bottom node
    median_values = {}
    for node, positions in neighbors.items():
        if positions:
            sorted_positions = sorted(positions)
            n = len(sorted_positions)
            # Compute median
            if n % 2 == 1:
                median_values[node] = sorted_positions[n // 2]
            else:
                median_values[node] = (sorted_positions[n // 2 - 1] + sorted_positions[n // 2]) / 2
        else:
            median_values[node] = float('inf')  # Nodes with no neighbors go to the end
    
    # Sort bottom nodes by their median values
    sorted_bottom_nodes = sorted(bottom_nodes, key=lambda x: median_values[x])
    
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
    
def permutation_patarasuk(fixed_layer, free_layer, edges):
    """
    Find the optimal ordering of the free layer to minimize edge crossings. Randomization for ties. 

    Parameters:
    - fixed_layer: List of vertices in the fixed layer (fixed order).
    - free_layer: List of vertices in the free layer.
    - edges: List of dictionaries with 'nodes' key, each containing a list of two vertices representing an edge.

    Returns:
    - Optimal ordering of free_layer with minimal crossings.
    - Minimum number of crossings.
    """
    min_crossings = float('inf')
    optimal_ordering = None
    # print("Currently has", len(fixed_layer), "vertices",  edges)
    for perm in permutations(free_layer):
        current_crossings = cross_count_optimized(fixed_layer, list(perm), edges)
        if current_crossings < min_crossings:
            min_crossings = current_crossings
            optimal_ordering = perm
        elif current_crossings == min_crossings:
            # 50% chance to accept the new permutation even if it's a tie
            if random.random() < 0.5:
                optimal_ordering = perm
                
    return list(optimal_ordering), min_crossings


def permutation(fixed_layer, free_layer, edges):
    """
    Find the optimal ordering of the free layer to minimize edge crossings.

    Parameters:
    - fixed_layer: List of vertices in the fixed layer (fixed order).
    - free_layer: List of vertices in the free layer.
    - edges: List of dictionaries with 'nodes' key, each containing a list of two vertices representing an edge.

    Returns:
    - Optimal ordering of free_layer with minimal crossings.
    - Minimum number of crossings.
    """
    min_crossings = float('inf')
    optimal_ordering = None
    # print("Currently has", len(fixed_layer), "vertices",  edges)
    for perm in permutations(free_layer):
        current_crossings = cross_count_optimized(fixed_layer, list(perm), edges)
        if current_crossings < min_crossings:
            min_crossings = current_crossings
            optimal_ordering = perm

    return list(optimal_ordering), min_crossings