import os
import sys
from bipartite_graph_generator import forced_density_gen_bip_graph, visualize_bipartite_graph

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from two_layer_functions.two_layer_barycenter import barycenter, parse_edges

# Generate a bipartite graph with 6 nodes per layer and 50% edge density
nodes, edges, B, top_nodes, bottom_nodes = forced_density_gen_bip_graph(n1=6, n2=6, density=0.4)

# Visualize the generated bipartite graph: BEFORE
visualize_bipartite_graph(B, bottom_nodes, title="Before Barycenter")

parsed_edges = parse_edges(edges, top_nodes, bottom_nodes)
bottom_nodes_bary = barycenter(bottom_nodes, top_nodes, parsed_edges)

# Visualize the generated bipartite graph: AFTER
visualize_bipartite_graph(B, bottom_nodes_bary, title="After Barycenter")
