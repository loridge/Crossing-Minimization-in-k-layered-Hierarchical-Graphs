import sys
import os
import random
import json
import copy
import time
import pandas as pd
import numpy as np
import math
import networkx as nx 
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from itertools import combinations, permutations
from typing import Dict, Union, List, Set
from concurrent.futures import ProcessPoolExecutor
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

densities = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

for density in densities:
    for i in range(4):
        nodes, edges, B, top, bottom = forced_density_gen_bip_graph(5,5, density)
        print(f"density: ", nx.bipartite.density(B, top))
        
        
# density: 0.12
# density: 0.12
# density: 0.12
# density: 0.12
# density: 0.2
# density: 0.2
# density: 0.2
# density: 0.2
# density: 0.32
# density: 0.32
# density: 0.32
# density: 0.32
# density: 0.4
# density: 0.4
# density: 0.4
# density: 0.4
# density: 0.52
# density: 0.52
# density: 0.52
# density: 0.52
# density: 0.6
# density: 0.6
# density: 0.6
# density: 0.6
# density: 0.72
# density: 0.72
# density: 0.72
# density: 0.72
# density: 0.8
# density: 0.8
# density: 0.8
# density: 0.8
# density: 0.92
# density: 0.92
# density: 0.92
# density: 0.92