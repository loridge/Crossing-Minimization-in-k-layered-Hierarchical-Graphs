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

from two_layer_functions.two_layer_barycenter import barycenter, parse_edges, median
from utility.bipartite_graph_generator import (
    count_crossings,
    update_positions,
    plot_results,
    generate_bipartite_graph,
    visualize_bipartite_graph
)
from sifting.sifting_2 import sifting
from sifting.crossing_function.crossing_func import cross_count

def branch_and_bound_oscm(fixed_layer, free_layer, edges, verbose=0):
    """
    Finds an ordering of the free_layer that minimizes edge crossings with the fixed_layer
    using a branch and bound algorithm.

    Parameters:
        fixed_layer: List of nodes in the fixed layer (can be integers or strings in the format 'uX').
        free_layer: List of nodes in the free layer (can be integers or strings in the format 'uX').
        edges: List of dictionaries representing edges, e.g. {'nodes': ['u1', 'u4']}.
        verbose: (Optional) Integer controlling verbosity (default is 0).

    Returns:
        A list representing the optimal ordering of the free_layer nodes as integers.
    """
    # Convert fixed_layer and free_layer nodes to string format "uX" if they are integers.
    fixed_layer = [f"u{node}" if isinstance(node, int) else node for node in fixed_layer]
    free_layer = [f"u{node}" if isinstance(node, int) else node for node in free_layer]

    # Precompute the "free degree" for each free-layer node:
    # Count the number of edges where the free node (assumed to be at position 1 in edge['nodes'])
    free_degree = {node: sum(1 for edge in edges if edge['nodes'][1] == node)
                   for node in free_layer}

    best_solution = {'order': None, 'crossings': float('inf')}

    def lower_bound(partial_order, remaining_nodes):
        """
        Compute a lower bound on the crossing count for any complete ordering extending partial_order.
        Here, we append the remaining nodes sorted by their free degree (in descending order) to form
        an optimistic candidate ordering.
        """
        # Sort remaining nodes by free_degree (higher degree nodes first)
        sorted_remaining = sorted(remaining_nodes, key=lambda node: free_degree[node], reverse=True)
        candidate_order = partial_order + sorted_remaining
        return cross_count(fixed_layer, candidate_order, edges)

    def recursive_search(partial_order, remaining_nodes):
        """
        Recursively builds the free_layer ordering, pruning branches that cannot beat
        the current best solution.
        """
        if verbose:
            print("Partial order:", partial_order, "Remaining:", remaining_nodes)
            
        # If no nodes remain, we've completed an ordering.
        if not remaining_nodes:
            total_crossings = cross_count(fixed_layer, partial_order, edges)
            if verbose:
                print("Complete order:", partial_order, "has crossings:", total_crossings)
            if total_crossings < best_solution['crossings']:
                best_solution['order'] = list(partial_order)
                best_solution['crossings'] = total_crossings
            return

        # Prune this branch if the lower bound is already worse than our best solution.
        lb = lower_bound(partial_order, remaining_nodes)
        if verbose:
            print("Lower bound for", partial_order, "with", remaining_nodes, "=", lb)
        if lb >= best_solution['crossings']:
            if verbose:
                print("Pruning branch:", partial_order, "remaining:", remaining_nodes)
            return

        # Otherwise, try adding each node from remaining_nodes to partial_order.
        for node in list(remaining_nodes):
            new_partial = partial_order + [node]
            new_remaining = remaining_nodes.copy()
            new_remaining.remove(node)
            recursive_search(new_partial, new_remaining)

    # Begin recursive search with an empty ordering.
    recursive_search([], free_layer.copy())

    # Convert best_solution['order'] to integers if they follow the "uX" format.
    if best_solution['order'] is not None:
        best_order_int = [
            int(node[1:]) if isinstance(node, str) and node.startswith('u') and node[1:].isdigit() else node
            for node in best_solution['order']
        ]
    else:
        best_order_int = None

    return best_order_int
