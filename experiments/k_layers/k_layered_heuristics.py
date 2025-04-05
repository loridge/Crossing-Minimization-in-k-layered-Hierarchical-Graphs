import random
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import sys, os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
# for i in sys.path:
#     print(i)

from sifting import (
    sifting,
)

from bary_med.two_layer_barycenter import (
    barycenter,
    parse_edges,
)

from k_layered import (
    generate_k_layered_sparse_graph,
    visualize_k_layered_graph,
    save_k_layered_graph,
)

from k_layer_crossing import (
    total_crossing_count_k_layer,
)

def update_k_layered_graph(G, edges):
    # is dis needed
    pass

def hybrid_2(layers, edges: list[list], l_cutoff):
    """Hybrid 2 k-layer heuristic

    Args:
        layers (_type_): _description_
        edges (_type_): in the dictionary format
        l_cutoff (_type_): _description_
    Returns:
        new_ordering_layers:
    """

    # or wait is l the index of the layer where the last sifting will be sweeped
    # layer by layer, sifting, then one barycenter sweep down
    # 0,1,2,3,4,5,6,7,8,9, are the indices of the layer
    # layer cutoff is the last layer that 
    
    # if l is the index of the layer where the last sifting will be sweeped, then all possible values must only be 1 to n-1 where n is len(layer_list)
    # if l is 0, then all barycenter(?)(?)
    # hence we implement a check here 
    if (0 <= l_cutoff <= (len(layers) - 1)) is False: # check this part
        print(f"Invalid l_cutoff value, it must be from 1 to {len(layers) - 1}")
        exit(0)
    
    forgiveness_number = 25 # recheck sa paper
    
    # 2 tasks
    # implement barycenter 1 sweep down
    # implement sifting up and down sweep
    
    listify_layers = [list(i) for i in layers]
    map_idx_to_layer= {index: sublist for index, sublist in enumerate(listify_layers)}
    map_node_to_layer = {node: index_i for index_i, sublist in map_idx_to_layer.items() for _, node in enumerate(sublist)}
    
    # the dict indices will be layers 1 to n-1
    layerfy_edges={i:[] for i in range(1,k)}  # O(1) access 3:[nodes list], para hindi na lagi mag O(n) search for an edge
    for edge_obj in edges:
        u, v = edge_obj['nodes'] # uX, uY
        # i want to check it in the listify layer
        u_id = int(u[1:])  # Remove 'u' and convert to integer
        v_id = int(v[1:])
        # u and v cannot be in the same layer. hence we may check only the larger of the two nodes; corresponds to our definition of layerfy
        greater_id = u_id if u_id > v_id else v_id # guaranted that the nodes are from 1 to n-1 where n is len of layer list
        
        layerfy_edges[map_node_to_layer[greater_id]].append(edge_obj)
        
    
    #### sifting sweep up down
    ## what is the definition of a 'sweep' again?
    
    min_crossings = total_crossing_count_k_layer(layers, edges)
    current_crossings = float('inf')
    
    # print(f"The layers are {listify_layers}")
    if l_cutoff != 0:
        print("Implementing the sifting sweeps.\n")
        while (forgiveness_number != 0):
            # determine what a sweep is, and refactor this at the soonest
            
            # down sweep
            for i in range(1, l_cutoff + 1): # [1, l_cutoff] is the real range
                # i are the indices of the free_layers in the downward sweep
                # print(f"At iter {i}, the bottom_nodes are {listify_layers[i]}")
                reordered_layer = sifting(listify_layers[i], listify_layers[i - 1], layerfy_edges[i])
                listify_layers[i] = reordered_layer
                # print(f"Downward sweep {i}, {listify_layers}")
                
            current_crossings = total_crossing_count_k_layer(listify_layers, edges)
            
            
            if current_crossings < min_crossings:
                min_crossings = current_crossings ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
            else: # current >= min # did not improve or worse.
                forgiveness_number -= 1
                
            if forgiveness_number == 0: break
            
            # up sweep
            for j in range(l_cutoff - 1, -1, -1): # [l_cutoff - 1, 0] is the real range
                # j should be the indices of the 'top_layer' that is the free_layer in upward sweep
                # print(f"At iter {j}, the free_nodes are {listify_layers[j]}")
                # print(f"Listify layer {j}:{listify_layers[j]}, {j+1}:{listify_layers[j+1]}, {layerfy_edges[j+1]}")
                reordered_layer = sifting(listify_layers[j], listify_layers[j + 1], layerfy_edges[j+1], 'upward')
                listify_layers[j] = reordered_layer
                # print(f"upward sweep {j}, {listify_layers}")
            
            current_crossings = total_crossing_count_k_layer(listify_layers, edges)
            
            if current_crossings < min_crossings:
                min_crossings = current_crossings   ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
            else: # current >= min # did not improve or worse.
                forgiveness_number -= 1
                
            if forgiveness_number == 0: break
    
    #### barycenter one sweep
    if l_cutoff != (len(layers) - 1):
        print("Implementing barycenter sweep \n")
        for layer_idx in range(l_cutoff + 1, len(layers)):
            #l_cutoff+1 because we want all the 'lower' layers, len(edges) because max_idx+1=len(deges)
            formatted_edges = parse_edges(edges, listify_layers[layer_idx - 1], listify_layers[layer_idx])
            baryed_free_layer = barycenter(listify_layers[layer_idx], listify_layers[layer_idx - 1], formatted_edges)
            listify_layers[layer_idx] = baryed_free_layer
        
    return listify_layers
    # update pos after all rearrangements has been made, for the sake of the graph visualizer
    
    ##### 
    
    

if __name__ == "__main__":
    k = 10
    n = 6
    m = 6
    nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, m)
    # print(nodes, layers)

    l_cutoff = 5
    new_layers = hybrid_2(layers, edges, l_cutoff)
    
    a = total_crossing_count_k_layer(layers, edges)
    print(a)
    save_k_layered_graph(G, layers, "old", a)
    b = total_crossing_count_k_layer(new_layers, edges)
    print(b)
    save_k_layered_graph(G, new_layers, "new", b)