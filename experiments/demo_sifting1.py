import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
from sifting.sifting_2 import sifting
from sifting.crossing_function import cross_count
from utility.bipartite_graph_generator import visualize_bipartite_graph, generate_bipartite_graph, update_positions
from bary_med.two_layer_barycenter import draw_horizontal_bipartite

nodes, edges, B, top_nodes, bottom_nodes = generate_bipartite_graph(4,3,0.3)


init_xsing = cross_count(top_nodes, bottom_nodes, edges)
print("demo1.py: initial crossings =", init_xsing)
draw_horizontal_bipartite(B, top_nodes, bottom_nodes, "Pre-Sifting")

new_free_layer = sifting(bottom_nodes, top_nodes, edges, verbose=0)
new_pos = update_positions(top_nodes, new_free_layer)
print("new pos", new_pos)
post_sifting_xsing = cross_count(top_nodes, new_free_layer, edges)
print("demo1.py: final crossings = ", post_sifting_xsing)
draw_horizontal_bipartite(B, top_nodes, new_free_layer, "Post-Sifting")