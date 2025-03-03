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

# Add the parent directory to sys.path to enable package imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from bary_med.two_layer_barycenter import barycenter, parse_edges, median
from utility.bipartite_graph_generator import (
    count_crossings,
    update_positions,
    plot_results,
    generate_bipartite_graph,
    visualize_bipartite_graph
)
from sifting.sifting_2 import sifting
from branch_bound import branch_and_bound_oscm

from sifting.crossing_function.crossing_func import cross_count

# Parameters for experimentation
vertex_counts = [10,20,30,40,50,60,]  # Example vertex counts for testing
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
    for i, top in enumerate(top_nodes):
        bottom = bottom_list[i % n2]  # Ensure at least one connection
        edges.add((top, bottom))
        B.add_edge(top, bottom)  # Add to graph

    # Ensure each bottom node has at least one connection
    top_list = list(top_nodes)
    random.shuffle(top_list)
    for i, bottom in enumerate(bottom_nodes):
        top = top_list[i % n1]  # Ensure at least one connection
        edges.add((top, bottom))
        B.add_edge(top, bottom)  # Add to graph

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

    for perm in permutations(free_layer):
        current_crossings = cross_count(fixed_layer, list(perm), edges)
        if current_crossings < min_crossings:
            min_crossings = current_crossings
            optimal_ordering = perm

    return list(optimal_ordering), min_crossings

def run_experiment(n1, n2):
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

        pos_original = nx.bipartite_layout(B, top_nodes, align="horizontal")
        crossings_original = count_crossings(B, pos_original)

        parsed_edges = parse_edges(edges, top_nodes, bottom_nodes)
        bottom_nodes_bary = barycenter(bottom_nodes, top_nodes, parsed_edges)
        pos_barycenter = update_positions(top_nodes, bottom_nodes_bary)
        crossings_barycenter = count_crossings(B, pos_barycenter)

        bottom_nodes_median = median(bottom_nodes, top_nodes, parsed_edges)
        pos_median = update_positions(top_nodes, bottom_nodes_median)
        crossings_median = count_crossings(B, pos_median)

        sifting_heuristic = sifting(list(bottom_nodes), list(top_nodes), edges, verbose=0)
        pos_sifting = update_positions(top_nodes, sifting_heuristic)
        crossings_sifting = count_crossings(B, pos_sifting)

        print("DEBUG-executing brute force method.")
        # _, crossings_optimal = minimize_crossings(list(top_nodes), list(bottom_nodes), edges)
        bottom_nodes_bb = branch_and_bound_oscm(top_nodes, bottom_nodes, edges, verbose=1)
        crossings_optimal = cross_count(top_nodes, bottom_nodes_bb, edges)
        
        
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
 
if __name__ == '__main__':
    start_time = time.time()

    all_results = []

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_experiment, n, n) for n in vertex_counts]

        for future in futures:
            all_results.append(future.result())

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")

    # Convert results to a DataFrame for analysis
    df = pd.DataFrame(all_results)

    # Display results
    print(df)

    # Save the results to a CSV file
    df.to_csv('experiment_results.csv', index=False)
    print("Results saved to 'experiment_results.csv'.")

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(df["n1"], df["avg_crossings_original"], label="Original")
    plt.plot(df["n1"], df["avg_crossings_barycenter"], label="Barycenter")
    plt.plot(df["n1"], df["avg_crossings_median"], label="Median")
    plt.plot(df["n1"], df["avg_crossings_sifting"], label="Sifting")
    plt.plot(df["n1"], df["avg_crossings_optimal"], label="Optimal (Brute-force)")

    plt.xlabel("Number of Vertices (|V1| = |V2|)")
    plt.ylabel("Average Number of Crossings")
    plt.title("Comparison of Crossing Minimization Algorithms")
    plt.legend()
    plt.grid(True)
    plt.savefig("crossing_minimization_results.png")
    plt.show()