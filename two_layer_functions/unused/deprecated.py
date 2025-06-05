import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import os
import random
import itertools
import math

def forced_density_gen_bip_graph(n1, n2, density):
    """
    Generate a bipartite graph with a fixed edge density.

    Args:
        n1 (int): Number of nodes in the first layer.
        n2 (int): Number of nodes in the second layer.
        density (float): Desired edge density (0 to 1).

    Returns:
        tuple: (nodes, edges, B, top_nodes, bottom_nodes)
            - nodes: List of dictionaries with "id" (prefixed "u") and "depth".
            - edges: List of dictionaries with "nodes" as a pair of "u"-prefixed IDs.
            - B: The NetworkX bipartite graph (with integer node IDs).
            - top_nodes: Set of integers (nodes in the first layer).
            - bottom_nodes: Set of integers (nodes in the second layer).
    """
    assert 0 <= density <= 1, "Density must be between 0 and 1"

    # Create an empty bipartite graph
    B = nx.Graph()

    # Define integer node IDs for the two sets
    top_nodes = set(range(1, n1 + 1))  # First layer
    bottom_nodes = set(range(n1 + 1, n1 + n2 + 1))  # Second layer

    B.add_nodes_from(top_nodes, bipartite=0)
    B.add_nodes_from(bottom_nodes, bipartite=1)

    # Compute the correct number of edges based on density
    max_edges = n1 * n2  # Maximum possible edges in a bipartite graph
    num_edges = int(density * max_edges)  # Target number of edges

    # Generate all possible edges and sample from them
    possible_edges = [(u, v) for u in top_nodes for v in bottom_nodes]
    selected_edges = random.sample(possible_edges, min(num_edges, len(possible_edges)))

    # Add selected edges to the graph
    B.add_edges_from(selected_edges)

    # Convert nodes into JSON format (with "u" prefix)
    nodes = [{"id": f"u{node}", "depth": 0 if node in top_nodes else 1} for node in B.nodes()]

    # Convert edges into JSON format (with "u" prefix)
    edges = [{"nodes": [f"u{u}", f"u{v}"]} for u, v in B.edges()]

    return nodes, edges, B, top_nodes, bottom_nodes