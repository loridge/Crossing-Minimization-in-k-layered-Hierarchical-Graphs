
import networkx as nx
from networkx.readwrite import json_graph
import json, sys,os
import time
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
with open("bipartite_graph.json", "r") as f:
    loaded_data = json.load(f)

# Reconstruct the graph
B_loaded = json_graph.node_link_graph(loaded_data["graph"])

# Retrieve other data
nodes = loaded_data["nodes"]
edges = loaded_data["edges"]
top_nodes = loaded_data["top_nodes"]
bottom_nodes = loaded_data["bottom_nodes"]

visualize_bipartite_graph(B_loaded, bottom_nodes, "old")

sift_bot = sifting(bottom_nodes, top_nodes, edges)

visualize_bipartite_graph(B_loaded, sift_bot, "sifted")

parsed_edge=parse_edges(edges, top_nodes, bottom_nodes)
bary_bot = barycenter(bottom_nodes, top_nodes, parsed_edge)
visualize_bipartite_graph(B_loaded, bary_bot, "preprocessed")

post_bary = sifting(bary_bot, top_nodes, edges)
visualize_bipartite_graph(B_loaded, post_bary, "bary+sift")