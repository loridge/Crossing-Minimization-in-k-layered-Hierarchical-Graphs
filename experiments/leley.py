
import networkx as nx
import random, math
from networkx.readwrite import json_graph
import json, sys,os
import time
from exp1_v1_v2_sparse_helper import generate_sparse_bipartite_graph
# Load JSON file
# Add the parent directory to sys.path to enable package imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
from bary_med.two_layer_barycenter import barycenter, parse_edges, median
from sifting.sifting_2 import sifting
from utility.bipartite_graph_generator import (
    count_crossings,
    update_positions,
    plot_results,
    generate_bipartite_graph,
    visualize_bipartite_graph
)

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

# with open("bipartite_graph.json", "r") as f:
#     loaded_data = json.load(f)

# # Reconstruct the graph
# B_loaded = json_graph.node_link_graph(loaded_data["graph"])

# # Retrieve other data
# nodes = loaded_data["nodes"]
# edges = loaded_data["edges"]
# top_nodes = loaded_data["top_nodes"]
# bottom_nodes = loaded_data["bottom_nodes"]

# visualize_bipartite_graph(B_loaded, bottom_nodes, "old")

# sift_bot = sifting(bottom_nodes, top_nodes, edges)

# visualize_bipartite_graph(B_loaded, sift_bot, "sifted")

# parsed_edge=parse_edges(edges, top_nodes, bottom_nodes)
# bary_bot = barycenter(bottom_nodes, top_nodes, parsed_edge)
# visualize_bipartite_graph(B_loaded, bary_bot, "preprocessed")

# post_bary = sifting(bary_bot, top_nodes, edges)
# visualize_bipartite_graph(B_loaded, post_bary, "bary+sift")

# --------------------------------------
# SPARSE GRAPHS
# nodes, edges, B, top_nodes, bottom_nodes = generate_sparse_bipartite_graph(3, 3)
# visualize_bipartite_graph(B, bottom_nodes, "sparse bipartite graph")

# nodes, edges, B, top_nodes, bottom_nodes = generate_sparse_bipartite_graph(4, 4)
# visualize_bipartite_graph(B, bottom_nodes, "sparse n-m bipartite graph")

nodes, edges, B, top_nodes, bottom_nodes = forced_density_gen_bip_graph(4, 4, 0.3)
visualize_bipartite_graph(B, bottom_nodes, "4-4 30% dense bipartite graph")

parsed_edges = parse_edges(edges, top_nodes, bottom_nodes)
bary_bot = barycenter(bottom_nodes, top_nodes, parsed_edges)
visualize_bipartite_graph(B, bary_bot, "barycenter")

median_bot = median(bottom_nodes, top_nodes, parsed_edges)
visualize_bipartite_graph(B, median_bot, "median")
