import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from concurrent.futures import ProcessPoolExecutor
import os
import sys
import time
from itertools import permutations
import random
import numpy as np

# Add the parent directory to sys.path to enable package imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from two_layer_functions.two_layer_barycenter import barycenter, parse_edges, median
from utility.bipartite_graph_generator import (
    count_crossings,
    update_positions,
    plot_results,
    generate_bipartite_graph,
    visualize_bipartite_graph
)
from sifting.sifting_2 import sifting
from branch_bound import branch_and_bound_oscm

from sifting.crossing_function.crossing_func import cross_count, cross_count_optimized


import json
from networkx.readwrite import json_graph

import math
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

    # Step 1: Ensure each node gets at least one connection
    top_list = list(top_nodes)
    bottom_list = list(bottom_nodes)
    random.shuffle(top_list)
    random.shuffle(bottom_list)

    # note that katapat nya yung meron, 
    for i in range(max(n1, n2)):
        u = top_list[i % n1]  # Cycle through top nodes
        v = bottom_list[i % n2]  # Cycle through bottom nodes
        edges.add((u, v))
        B.add_edge(u, v)

    # Step 2: Distribute remaining edges evenly across the vertices
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

# Assume B is your NetworkX bipartite graph and other structures exist
nodes, edges, B, top_nodes, bottom_nodes = forced_density_gen_bip_graph(10,10,0.2)

# Convert graph B to a JSON-compatible format
graph_data = json_graph.node_link_data(B)

# Store all relevant data in a dictionary
data_to_save = {
    "graph": graph_data,
    "nodes": list(nodes),
    "edges": edges,
    "top_nodes": list(top_nodes),
    "bottom_nodes": list(bottom_nodes)
}

# Save to a JSON file
with open("bipartite_graph.json", "w") as f:
    json.dump(data_to_save, f, indent=4)