# from copy import deepcopy
# import networkx as nx
# import matplotlib.pyplot as plt
# import json
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sifting_2 import sifting
from barycenter.bipartite_graph_generator import generate_bipartite_graph, visualize_bipartite_graph, update_positions 
from barycenter.two_layer_barycenter import draw_horizontal_bipartite
from crossing_function.crossing_func import cross_count
# Graph Configuration
n1 = 4
n2 = 4
p = 0.1

nodes, edges, B, top_nodes, bottom_nodes = generate_bipartite_graph(n1,n2,p)

print("nodes", nodes)
print("edges", edges)
print("top", top_nodes)
print("bottom",bottom_nodes)


print("Printing before")
visualize_bipartite_graph(B, bottom_nodes)
# print(cross_count(list(top_nodes), list(bottom_nodes), edges))
print(cross_count((top_nodes), (bottom_nodes), edges))

fixed_layer = top_nodes
free_layer = bottom_nodes

sift_res = sifting(free_layer, fixed_layer, edges, verbose=0,)
minimized_layer = sift_res
# print(cross_count(list(top_nodes), list(minimized_layer), edges))
print(cross_count((top_nodes), (minimized_layer), edges))
draw_horizontal_bipartite(B, top_nodes,  minimized_layer, "After Sift Algorithm")


print("**********************************")
print("Original layer:")
print(free_layer)
print("Minimized layer:")
print(minimized_layer)