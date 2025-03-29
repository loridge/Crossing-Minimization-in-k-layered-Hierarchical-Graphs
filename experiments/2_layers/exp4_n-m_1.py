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
import itertools
from networkx.algorithms import bipartite
from itertools import combinations, permutations
from typing import Dict, Union, List, Set
from concurrent.futures import ProcessPoolExecutor

"""
    Notes: 
    - May difference pa rin between the actual density and predicted density. This is more prominent in sparse graphs. Its either we ceiling or floor the 
    number of edges. e.g. 0.1 density n=4,m=2. 0.1*n*m=0.8. but num_edges=1. 1/8=0.125 actual density
    
    -Sifting used here is not adjusted to isolate the singletons in one side. this might affect the solution in k-layered graphs
"""


# Graph_Utilities/Graph Generators
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
    # num_edges=max(1,min(int(math.floor(density * max_edges)), max_edges))
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

# Graph_Utilities/Utilities
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

def binary_search_first_smaller(arr, v, lower_bound, upper_bound, index_references, v_index):
    """
    Binary search to find the rightmost index in 'arr' where the value is smaller than 'v'.
    The search starts from 'lower_bound' and ends at 'upper_bound' to optimize performance.

    Args:
        arr (list[str]): The sorted list of neighbor nodes.
        v (str): The node to compare against.
        lower_bound (int): The starting index for the search.
        upper_bound (int): The ending index for the search.
        index_references (dict): Dictionary mapping nodes to their fixed_layer indices.
        v_index (int): The index of the node 'v' in the fixed layer.

    Returns:
        int: The index of the last element smaller than 'v', or -1 if none exist.
    """
    left, right = lower_bound, upper_bound
    result = -1  # Default to -1 (not found)

    while left <= right:  # Fix condition to include rightmost element
        mid = (left + right) // 2
        # print(f"DEBUG INSIDE BINSEARCH arr[mid]: {arr[mid]}, left: {left}, right: {right}, mid: {mid}")

        if index_references[arr[mid]] < v_index:
            result = mid  # Update result, but keep searching to the right
            left = mid + 1
        else:
            right = mid - 1  # Move left to find a smaller value

    return result  # Final rightmost valid index

def cross_count_optimized(fixed_layer: list[str], free_layer: list[str], edges: list):
    crossing_total = 0
    
    fixed_layer = [f"u{node}" if isinstance(node, int) else node for node in list(fixed_layer) ]
    free_layer =  [f"u{node}" if isinstance(node, int) else node for node in list(free_layer) ]

    fixed_layer_dict = {node: index for index, node in enumerate(fixed_layer)}
    free_layer_dict = {node: index for index, node in enumerate(free_layer)}

    neighbor_dict = {node: [] for node in free_layer}
    easy_free = set(free_layer)
    easy_fixed = set(fixed_layer)

    for edge_data in edges:
        u, v = edge_data["nodes"]
        if u in easy_free and v in easy_fixed:
            neighbor_dict[u].append(v)
        elif v in easy_free and u in easy_fixed:
            neighbor_dict[v].append(u)

    # Sort neighbors based on their position in fixed_layer
    for node in neighbor_dict:
        neighbor_dict[node].sort(key=lambda x: fixed_layer_dict[x])

    #### CROSSING PROPER ####
    for i, u_node in enumerate(free_layer):
        u_neighbors = neighbor_dict[u_node]
        u_prime_nodes = free_layer[i + 1:]
        # print("")
        # print("u_node ", u_node, ";;;u_prime nodes > u_node: ",u_prime_nodes)
        for u_prime in u_prime_nodes:
          u_prime_neighbors = neighbor_dict[u_prime]
          lb = 0   # 0 indexed as opposed to pseudocode
          ub = len(u_prime_neighbors) - 1  # 0 indexed as opposed to pseudocode
          # print(f"DEBUG u-prime-neighbors: {u_prime_neighbors} of u-prime {u_prime}")
          for v in u_neighbors:
              result = binary_search_first_smaller(u_prime_neighbors, v, lb, ub, fixed_layer_dict, fixed_layer_dict[v]) ##, edit it must be based on indices not the values of the elements themselves
              if result != -1:
                crossing_total += result + 1

    return crossing_total

# Results
def plot_results_percentage_outliers(df, message="", save_dir="plot_results", filename=None):
    # (B, bottom_nodes, title, save_dir="graphs", filename=None)
    """
    Plots and Save the experiment results. Also includes optional message for the title.
    Each combination of n1 and n2 will have its own line for each heuristic,
    using graph density instead of edge probability on the x-axis.
    
    Args:
        df: Pandas DataFrame
        message: [optional] additional message in the plot title
        save_dir: The directory where the files will be saved
        filename: The custom filename for all files
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
                plt.title(f"Crossings for n1={n1}, n2={n2}, {message}")
                plt.xlabel("Graph Density")
                plt.ylabel("In percentage of the minimum number of crossings")
                plt.legend()
                plt.grid(True)
                
                # Make directory
                os.makedirs(save_dir, exist_ok=True)
                
                # Make the file name
                if filename==None:
                    filename="plot_results"
                png_file=f"{filename}_results_{n1}+{n2}.png"
                csv_file=f'{filename}_results_{n1}+{n2}.csv'
                # join the new folder directory and the filename
                save_path_png = os.path.join(save_dir, png_file)
                save_path_csv = os.path.join(save_dir, csv_file)
                plt.savefig(save_path_png, dpi=300, bbox_inches="tight")
                df.to_csv(save_path_csv, index=False)
                
                # Show the plot
                # plt.show()
                plt.close()
                
# Heuristics/Permutation
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

# Heuristics/barycenter
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

# Heuristics/median
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

# Heuristics/sifting
def sifting(bottom_nodes, top_nodes, edges, verbose=0):
    """
    Reorders bottom nodes using the sifting heuristic based on indegree in decreasing order.
    
    Parameters:
    - bottom_nodes: List of bottom-layer nodes.
    - top_nodes: List of top-layer nodes.
    - edges: List of dictionaries representing edges with format {'nodes': ['uX', 'uY']}.
    
    Returns:
    - Reordered list of bottom-layer nodes as integers.
    """
    
    top_nodes = [f"u{node}" if isinstance(node, int) else node for node in list(top_nodes) ]
    bottom_nodes = [f"u{node}" if isinstance(node, int) else node for node in list(bottom_nodes) ]  
    
    # Compute indegree for each bottom node
    indegree = {node: 0 for node in bottom_nodes}
    for edge in edges:
        _, b = edge['nodes']
        indegree[b] += 1
    
    # Sort bottom nodes by indegree in decreasing order (priority queue for processing order)
    sorted_nodes = sorted(bottom_nodes, key=lambda node: -indegree[node])
    
    # Apply the sifting heuristic
    for node in sorted_nodes:
        best_position = bottom_nodes.index(node)
        best_crossings = cross_count_optimized(top_nodes, bottom_nodes, edges)
        
        for j in range(len(bottom_nodes)):
            if bottom_nodes[j] == node:
                continue
            
            # Swap node to new position
            bottom_nodes.remove(node)
            bottom_nodes.insert(j, node)
            current_crossings = cross_count_optimized(top_nodes, bottom_nodes, edges)
            
            if current_crossings < best_crossings:
                best_position = j
                best_crossings = current_crossings
            
            # Revert swap
            bottom_nodes.remove(node)
            bottom_nodes.insert(best_position, node)
    
    # Extract integer values from node labels
    return [int(node[1:]) if isinstance(node, str) and node.startswith('u') and node[1:].isdigit() else node for node in bottom_nodes]


# Experiments
def run_experiment(n1, n2, p, num_samples):
    total_density=0
    # total_density=[]
    total_actual_density=0
    max_edges=n1*n2
    result = {
        "n1": n1,
        "n2": n2,
        "num_samples": num_samples,
        "avg_actual_edges": 0,
        "max_edges": max_edges,
        "pred_density": None,
        "density": None,
        "avg_crossings_original": 0,
        "avg_crossings_barycenter": 0,
        "avg_crossings_median": 0,
        "avg_crossings_sifting": 0,
        "avg_crossings_optimal": 0
    }
    for _ in range(num_samples):
        # Generate bipartite graph
        nodes, edges, B, top_nodes, bottom_nodes = forced_density_gen_bip_graph(n1, n2, p)
        
        # Calculate density, not yet bipartite
        density = bipartite.density(B, set(top_nodes))
        total_density += density
        # total_density.append(density)
        
        num_edges = max(1, min(int(math.ceil(density * max_edges)), max_edges))  # Ensure valid range
        total_actual_density += num_edges
        
        crossings_original = crossings_median = cross_count_optimized(top_nodes, bottom_nodes, edges)

        # Parse the edges into (top_node, bottom_node) tuples before passing to the barycenter function
        parsed_edges = parse_edges(edges, top_nodes, bottom_nodes)
        
        # Apply Barycenter heuristic to reorder bottom nodes
        bottom_nodes_bary = barycenter(bottom_nodes, top_nodes, parsed_edges)

        # Update positions: top nodes fixed, bottom nodes reordered
        # pos_barycenter = update_positions(top_nodes, bottom_nodes_bary)
        # crossings_barycenter = count_crossings(B, pos_barycenter)
        crossings_barycenter = cross_count_optimized(top_nodes, bottom_nodes_bary, edges)

        # Apply Median heuristic to reorder bottom nodes
        bottom_nodes_median = median(bottom_nodes, top_nodes, parsed_edges)
        crossings_median = cross_count_optimized(top_nodes, bottom_nodes_median, edges)

        # Update positions: top nodes fixed, bottom nodes reordered
        # pos_median = update_positions(top_nodes, bottom_nodes_median)
        # crossings_median = count_crossings(B, pos_median)

        # Apply Simple Sifting heuristic to reorder bottom nodes
        sifting_heuristic = sifting(bottom_nodes, top_nodes, edges, verbose=0, )
        crossings_sifting = cross_count_optimized(top_nodes, sifting_heuristic,edges)
        
        bottom_nodes_optimal, crossings_optimal = minimize_crossings(list(top_nodes), list(bottom_nodes), edges)
        
        result["avg_crossings_original"] += crossings_original
        result["avg_crossings_barycenter"] += crossings_barycenter
        result["avg_crossings_median"] += crossings_median
        result["avg_crossings_sifting"] += crossings_sifting
        result["avg_crossings_optimal"] += crossings_optimal


    # Store results
    result["avg_actual_edges"] = total_actual_density / num_samples
    result["density"] = total_density / num_samples
    # result["density"]=max(total_density)
    result["pred_density"] = p
    result["avg_crossings_original"] /= num_samples
    result["avg_crossings_barycenter"] /= num_samples
    result["avg_crossings_median"] /= num_samples
    result["avg_crossings_sifting"] /= num_samples
    result["avg_crossings_optimal"] /= num_samples
    return result


if __name__ == '__main__':
    #- n is even (4 6 8 10)
    # - for every n, m is  range[n/2,n],step=1

    # all possible n values
    n_values=[4,6,8,10]

    # singleton experiment with n-m graphs
    for n in n_values:
        ########## EVERY EXPERIMENT IS UNDER N-M ############
        for m in range(n//2, n+1):
            print(f"Exp_4 {n}-{m} underway")
            start_time = time.time()
            
            
            results=[]
            num_samples = 10
            p_values = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
            with ProcessPoolExecutor() as executor:
                futures = []
                # for n1 in n1_values:
                #     for n2 in n2_values:
                for p in p_values:
                    print(f"Running experiment for n:{n}, m:{m}, p:{p}")
                    futures.append(executor.submit(run_experiment, n, m, p, num_samples))

                for future in futures:
                    results.append(future.result())
            
            end_time = time.time()
            total_time = end_time - start_time
            print(f"Total execution time: {total_time:.2f} seconds")
            
            df = pd.DataFrame(results)
            
            plot_results_percentage_outliers(df, f"{num_samples} Samples-generator is ceil", "exp4_n-m_1", 'exp4')
        print("\n")