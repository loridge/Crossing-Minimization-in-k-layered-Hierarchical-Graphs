from bipartite_graph_generator import generate_bipartite_graph, visualize_bipartite_graph, count_crossings, update_positions, plot_results
from two_layer_barycenter import barycenter, parse_edges, median, draw_horizontal_bipartite
from edgedensity import generator_bip_graph
from sifting_2 import sifting
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from crossing_func import cross_count
n1 = 10
n2 = 10
p = 0.2

# Generate bipartite graph
nodes, edges, B, top_nodes, bottom_nodes = generate_bipartite_graph(n1, n2, p)
# nodes, edges, B, top_nodes, bottom_nodes = generator_bip_graph(n1, n2, p, LA=1)

# Calculate density, not yet bipartite
# density = nx.density(B)
density = bipartite.density(B, set(top_nodes))
# Visualize the graph (optional, for small graphs)
#visualize_bipartite_graph(B, bottom_nodes)

# Original layout
pos_original = nx.bipartite_layout(B, top_nodes, align="horizontal")
crossings_original = count_crossings(B, pos_original)
print("crossings_oirg", crossings_original)
# Parse the edges into (top_node, bottom_node) tuples before passing to the barycenter function
parsed_edges = parse_edges(edges, top_nodes, bottom_nodes)

# Apply Barycenter heuristic to reorder bottom nodes
bottom_nodes_bary = barycenter(bottom_nodes, top_nodes, parsed_edges)

#visualize_bipartite_graph(B, bottom_nodes_bary)

# Update positions: top nodes fixed, bottom nodes reordered
pos_barycenter = update_positions(top_nodes, bottom_nodes_bary)
crossings_barycenter = count_crossings(B, pos_barycenter)
print("crossings_bary", crossings_barycenter)
# Apply Median heuristic to reorder bottom nodes
# bottom_nodes_median = median(bottom_nodes, top_nodes, parsed_edges)

# # Update positions: top nodes fixed, bottom nodes reordered
# pos_median = update_positions(top_nodes, bottom_nodes_median)
# # print("POS_MEDIAN", pos_median) #LELEY nilagay ko to
# crossings_median = count_crossings(B, pos_median)

#visualize_bipartite_graph(B, bottom_nodes_median)






# Apply Simple Sifting heuristic to reorder bottom nodes
# does not accept edges as tuples
sifting_heuristic = sifting(bottom_nodes, top_nodes, edges, verbose=0, LA_gen=1)

# draw_horizontal_bipartite(B, top_nodes, sifting_heuristic, "After Sift Algorithm") ## bug spotted, i also commented a code out in sifting
#LELEY inedit ko draw_horiz_bipartite, sifting ---> sifting_heuristics
pos_sifting = update_positions(top_nodes, sifting_heuristic) # the sifting_heuristic is 1,2,3,4,5 while the previous ones have 'u1, u2,..' 
# leley ninote ko lang yung pagdebug ko

# print("POS_SIFTING", pos_sifting)

# crossings_sifting = count_crossings(B, pos_sifting)
crossings_sifting = cross_count(top_nodes, sifting_heuristic, edges, LA_gen=1)
print("crossings_sifting", crossings_sifting)