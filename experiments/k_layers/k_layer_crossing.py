import sys, os
import json
from networkx.readwrite import json_graph

# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# debugging module imports
print("from k layer crossing", parent_dir)
# print("Current working dir:", os.getcwd)
for i in sys.path:
    print(i)
# print("__file__:", __file__)
    
from sifting.crossing_function import (
    cross_count_optimized,
)
from k_layered import (
    visualize_k_layered_graph,
    generate_k_layered_sparse_graph,
)
def total_crossing_count_k_layer(layers, edges):
    # uses the nodes: [u1, u2] edges
    # layers are an array of sets
    
    # iba yung ordering na nakuha ko from the layers array. that D.S. cant be used, i have to find a way
    #### -> i have to find a way to use the actual ordering in the graph visualizer itself
    ### fixed due to the sorted() call in the visualizer commented out
    total_crossings=0
    for i in range(len(layers)-1):
        top_layer=list(layers[i])
        bottom_layer=list(layers[i+1])
        layer_crossing=cross_count_optimized(top_layer, bottom_layer, edges)
        total_crossings+=layer_crossing
        
    ### I believe we can accelerate this by dividing a k-layered graph recursively, sub problems instead of iterating every layer
    
    return total_crossings

def total_crossing_count_k_layers_speedup(layers, edges):
    #   reorderable layers = layers - 1 
    #   
    #
    #
    #
    #
    #
    #
    
    reorderable_layers = len(layers) - 1
    mid = reorderable_layers // 2
    if (len(layers)==2):
        return cross_count_optimized(layers[0], layers[1], edges)
    else:   
        return total_crossing_count_k_layers_speedup(layers[:mid],edges) + total_crossing_count_k_layers_speedup(layers[mid + 1:], edges)
    
    pass

if __name__=="__main__":
    k = 4  # Number of layers
    n = 5  # Number of vertices in odd layers
    m = 3  # Number of vertices in even layers  

    nodes, formatted_edges, G, layers = generate_k_layered_sparse_graph(k, n, m)
    # print(nodes)
    print(formatted_edges)
    print(layers)
    
    graph_data = json_graph.node_link_data(G)
    final_cnt=total_crossing_count_k_layer(layers, formatted_edges)
    print(f"Total crossings: {final_cnt}")
    # The layers are from 1 to 6
    visualize_k_layered_graph(G, layers, "K-Layered Sparse Graph")

# Save to a JSON file
    with open("bipartite_graph.json", "w") as f:
        json.dump(graph_data, f, indent=4)