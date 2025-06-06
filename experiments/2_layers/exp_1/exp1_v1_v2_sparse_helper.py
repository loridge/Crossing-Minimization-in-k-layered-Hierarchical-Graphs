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
from two_layer_functions.bipartite_graph_generator import (
    count_crossings,
    update_positions,
    plot_results,
    generate_bipartite_graph,
    visualize_bipartite_graph
)
from two_layer_functions.sifting_2 import sifting
# from branch_bound import branch_and_bound_oscm

from two_layer_functions.crossing_func import cross_count, cross_count_optimized

vertex_counts = [10,]  # Example vertex counts for testing
num_samples = 1  # Number of samples per vertex count

def generate_sparse_bipartite_graph(n1, n2):
    """
    Generate a sparse bipartite graph with |E| = |V1| + |V2|, ensuring no disconnected nodes.

    Parameters:
    - n1: Number of nodes in the first partition.
    - n2: Number of nodes in the second partition.

    Returns:
    - nodes: List of all nodes.
    - edges: List of edges formatted for heuristics (e.g., {'nodes': ['u1', 'u4']})
    - B: Generated bipartite graph.
    - top_nodes: Set of integers representing nodes in the first partition.
    - bottom_nodes: Set of integers representing nodes in the second partition.
    """
    B = nx.Graph()
    top_nodes = set(range(1, n1 + 1))
    bottom_nodes = set(range(n1 + 1, n1 + n2 + 1))
    B.add_nodes_from(top_nodes, bipartite=0)
    B.add_nodes_from(bottom_nodes, bipartite=1)

    edges = set()

    # Ensure each top node has at least one connection
    bottom_list = list(bottom_nodes)
    random.shuffle(bottom_list)  # Shuffle to randomize assignment
    # for i, top in enumerate(top_nodes):
    #     bottom = bottom_list[i % n2]  # Ensure at least one connection
    #     edges.add((top, bottom))
    #     B.add_edge(top, bottom)  # Add to graph

    # COMMENTED OUT TO ALLOW SINGLETONS
    # Ensure each bottom node has at least one connection
    top_list = list(top_nodes)
    # random.shuffle(top_list)
    # for i, bottom in enumerate(bottom_nodes):
    #     top = top_list[i % n1]  # Ensure at least one connection
    #     edges.add((top, bottom))
    #     B.add_edge(top, bottom)  # Add to graph

    # Add remaining edges until we reach |E| = |V1| + |V2|
    while len(edges) < (n1 + n2):
        top = random.choice(top_list)
        bottom = random.choice(bottom_list)
        if (top, bottom) not in edges:  # Avoid duplicates
            edges.add((top, bottom))
            B.add_edge(top, bottom)  # Add to graph

    # Convert edges to required format
    formatted_edges = [{'nodes': [f'u{u}', f'u{v}']} for u, v in edges]

    nodes = list(top_nodes | bottom_nodes)  # Combine and convert to a list

    return nodes, formatted_edges, B, top_nodes, bottom_nodes

def minimize_crossings(fixed_layer, free_layer, edges):
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

def run_experiment(n1, n2, num_samples):
    """
    Run experiments for a given pair of vertex counts.

    Parameters:
    - n1: Number of nodes in the first partition.
    - n2: Number of nodes in the second partition.

    Returns:
    - Dictionary containing the average number of crossings for each heuristic.
    """
    results = {
        "n1": n1,
        "n2": n2,
        "density": None,
        "avg_crossings_original": 0,
        "avg_crossings_barycenter": 0,
        "avg_crossings_median": 0,
        "avg_crossings_sifting": 0,
        "avg_crossings_optimal": 0
    }

    total_density = 0

    for _ in range(num_samples):
        nodes, edges, B, top_nodes, bottom_nodes = generate_sparse_bipartite_graph(n1, n2)
        
        density = bipartite.density(B, top_nodes)
        total_density += density

        analyze_graph(B)

        pos_original = nx.bipartite_layout(B, top_nodes, align="horizontal")
        # crossings_original = count_crossings(B, pos_original)
        crossings_original = cross_count_optimized(top_nodes, bottom_nodes, edges)
        parsed_edges = parse_edges(edges, top_nodes, bottom_nodes)
        
        
        bottom_nodes_bary = barycenter(bottom_nodes, top_nodes, parsed_edges)
        pos_barycenter = update_positions(top_nodes, bottom_nodes_bary)
        # crossings_barycenter = count_crossings(B, pos_barycenter)
        crossings_barycenter = cross_count_optimized(top_nodes, bottom_nodes_bary, edges)
        # if not (crossings_barycenter) == xsing_bary:
        #     print(f"Condition failed. Stopping execution for {density}.")
        #     sys.exit(1)
            
        bottom_nodes_median = median(bottom_nodes, top_nodes, parsed_edges)
        pos_median = update_positions(top_nodes, bottom_nodes_median)
        # crossings_median = count_crossings(B, pos_median)
        crossings_median = cross_count_optimized(top_nodes, bottom_nodes_median, edges)
        # if not (crossings_median) == xsing_med:
        #     print(f"Condition failed. Stopping execution for {density}.")
        #     sys.exit(1)

        sifting_heuristic = sifting(list(bottom_nodes), list(top_nodes), edges, verbose=0)
        pos_sifting = update_positions(top_nodes, sifting_heuristic)
        # crossings_sifting = count_crossings(B, pos_sifting)
        crossings_sifting = cross_count_optimized(top_nodes, sifting_heuristic, edges)
        # print((crossings_sifting) == better_crossing)
        # if not (crossings_sifting) == better_crossing:
        #     print(f"Condition failed. Stopping execution for {density}.")
        #     sys.exit(1)
        # print("DEBUG-executing brute force method.")
        bottom_nodes_optimal, crossings_optimal = minimize_crossings(list(top_nodes), list(bottom_nodes), edges)
        # bottom_nodes_bb = branch_and_bound_oscm(top_nodes, bottom_nodes, edges, verbose=1)
        # crossings_optimal = cross_count(top_nodes, bottom_nodes_bb, edges)
        
        
        results["avg_crossings_original"] += crossings_original
        results["avg_crossings_barycenter"] += crossings_barycenter
        results["avg_crossings_median"] += crossings_median
        results["avg_crossings_sifting"] += crossings_sifting
        results["avg_crossings_optimal"] += crossings_optimal

    # Compute averages
    results["density"] = total_density / num_samples
    results["avg_crossings_original"] /= num_samples
    results["avg_crossings_barycenter"] /= num_samples
    results["avg_crossings_median"] /= num_samples
    results["avg_crossings_sifting"] /= num_samples
    results["avg_crossings_optimal"] /= num_samples

    return results  # Ensure this line is present!

def analyze_graph(B):
    """
    Analyzes the degree distribution and connectivity of a bipartite graph.
    """
    degrees = dict(B.degree())
    degree_values = list(degrees.values())

    # Compute degree statistics
    avg_degree = np.mean(degree_values)
    max_degree = np.max(degree_values)
    min_degree = np.min(degree_values)
    #density = nx.density(B)   

    print(f"📊 Degree Analysis:", flush=True)
    print(f"Degrees are: {degrees}", flush=True) 
    print(f"   - Average Degree: {avg_degree:.2f} (Expected: ≈2)", flush=True)
    print(f"   - Max Degree: {max_degree}", flush=True)
    print(f"   - Min Degree: {min_degree}", flush=True)
    #print(f"   - Edge Density: {density:.4f}", flush=True)

    # Plot degree distribution
    # plt.hist(degree_values, bins=range(min_degree, max_degree + 1), align='left', edgecolor='black')
    # plt.xlabel("Degree")
    # plt.ylabel("Frequency")
    # plt.title("Degree Distribution")
    # plt.show()

    # Check if the graph is connected
    if nx.is_connected(B):
        print("✅ Graph is fully connected.")
    else:
        print(f"❌ Graph has {nx.number_connected_components(B)} connected components.")
