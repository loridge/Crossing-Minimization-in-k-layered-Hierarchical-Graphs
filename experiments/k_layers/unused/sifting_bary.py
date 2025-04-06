import random
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import sys, os
import copy

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
    permutation,
)

from k_layered import (
    generate_k_layered_sparse_graph,
    visualize_k_layered_graph,
)

from k_layer_crossing import (
    total_crossing_count_k_layer,
)

def hybrid_1_sift_bary(layers, edges) -> list[list]:
    """
    Hybrid_1.2 k_layer heuristics: Sifting + barycenter layer-by-layer sweep will be implemented.
    For free layers with size of 6 or lower, sifting will be applied. Else, barycenter. 
    

    Args:
        layers (_list[set] or list[list]_): List of lists of ordered nodes in
            every layer. The layers are 0-indexed, from 'top' to 'bottom.'

        edges (_type_): An exhaustive list of edge objects of the whole graph,
            formatted as {'nodes':[uX, uY]}.

    Returns:
        new_ordering_layers (_list[list]_): New reordering of nodes of each
            layer that reduces the number of crossings in the whole graph.
    """
    
    forgiveness_number = 40 # recheck sa paper
    threshold_size = 6
    k = len(layers)
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
    
    min_crossings = total_crossing_count_k_layer(layers, edges)
    current_crossings = 0
    
    
    while (forgiveness_number != 0):
        # down sweep
        for i in range(1, len(layers)-1): # [1, l_cutoff] is the real range
            # i are the indices of the free_layers in the downward sweep
            if len(listify_layers[i]) <= threshold_size:
                reordered_layer = sifting(listify_layers[i], listify_layers[i - 1], layerfy_edges[i])
            else:
                parsed_edges = parse_edges(layerfy_edges[i], listify_layers[i - 1], listify_layers[i])
                reordered_layer = barycenter(listify_layers[i], listify_layers[i - 1], parsed_edges)
            listify_layers[i] = reordered_layer
        
        # do we update the original listify_layers only if there is an improvement? so like do we copy the data structure then see if it imptoves.
        
        current_crossings = total_crossing_count_k_layer(listify_layers, edges)
        
        if current_crossings < min_crossings:
            min_crossings = current_crossings ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
        else: # current >= min # did not improve or worse.
            forgiveness_number -= 1
            
        if forgiveness_number == 0: break
        
        # up sweep
        for j in range(len(layers)-2, -1, -1): # [l_cutoff - 1, 0] is the real range
            # j should be the indices of the 'top_layer' that is the free_layer in upward sweep
            if len(listify_layers[j]) <= threshold_size:
                reordered_layer = sifting(listify_layers[j], listify_layers[j + 1], layerfy_edges[j+1], 'upward')
            else:
                parsed_edges = parse_edges(layerfy_edges[j+1], listify_layers[j + 1], listify_layers[j])
                reordered_layer = barycenter(listify_layers[j], listify_layers[j + 1], parsed_edges)
            listify_layers[j] = reordered_layer
        
        current_crossings = total_crossing_count_k_layer(listify_layers, edges)
        
        if current_crossings < min_crossings:
            min_crossings = current_crossings   ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
        else: # current >= min # did not improve or worse.
            forgiveness_number -= 1
            
        if forgiveness_number == 0: break
        
    return listify_layers

def hybrid_2_patarasuk(layers, edges: list[list], l_cutoff) -> list[list]:
    """
    Hybrid_2 k_layer heuristics: Sifting layer-by-layer sweep will be implemented
    for layers until the l_cutoff. All layers below the l_cutoff will be
    rearranged with barycenter, one down sweep.

    Args:
        layers (_list[set] or list[list]_): List of lists of ordered nodes in
            every layer. The layers are 0-indexed, from 'top' to 'bottom.'

        edges (_type_): An exhaustive list of edge objects of the whole graph,
            formatted as {'nodes':[uX, uY]}.

        l_cutoff (_int_): The index of the last layer that will be manipulated
            by sifting. Valid indices are 0 to maxLayerIndex.
            - 0 means all layers use barycenter.
            - maxLayerIndex means all layers use sifting sweep.

    Returns:
        new_ordering_layers (_list[list]_): New reordering of nodes of each
            layer that reduces the number of crossings in the whole graph.
    """

    # or wait is l the index of the layer where the last sifting will be sweeped
    # layer by layer, sifting, then one barycenter sweep down
    # 0,1,2,3,4,5,6,7,8,9, are the indices of the layer
    # layer cutoff is the last layer that 
    
    # if l is the index of the layer where the last sifting will be sweeped, then all possible values must only be 0 to n-1 where n is len(layer_list)
    # hence we implement a check here 
    if (0 <= l_cutoff <= (len(layers) - 1)) is False:
        print(f"Invalid l_cutoff value, it must be from 1 to {len(layers) - 1}")
        exit(0)
    
    forgiveness_number = 20 # recheck sa paper
    k = len(layers)
    # 2 tasks
    # implement barycenter 1 sweep down
    # implement sifting up and down sweep
    
    listify_layers = [list(i) for i in layers]
    map_idx_to_layer= {index: sublist for index, sublist in enumerate(listify_layers)}
    map_node_to_layer = {node: index_i for index_i, sublist in map_idx_to_layer.items() for _, node in enumerate(sublist)}
    
    # the dict indices will be layers 1 to n-1
    layerfy_edges={i:[] for i in range(1, k)}  # O(1) access 3:[nodes list], para hindi na lagi mag O(n) search for an edge
    
    for edge_obj in edges:
        u, v = edge_obj['nodes'] # uX, uY
        # i want to check it in the listify layer
        u_id = int(u[1:])  # Remove 'u' and convert to integer
        v_id = int(v[1:])
        # u and v cannot be in the same layer. hence we may check only the larger of the two nodes; corresponds to our definition of layerfy
        greater_id = u_id if u_id > v_id else v_id # guaranted that the nodes are from 1 to n-1 where n is len of layer list
        
        layerfy_edges[map_node_to_layer[greater_id]].append(edge_obj)
        
    # print(f"layerfy_edges {layerfy_edges}")
    
    #### sifting sweep up down
    ## what is the definition of a 'sweep' again?
    
    min_crossings = float('inf')
    best_layer_struct = copy.deepcopy(listify_layers)
    current_crossings = float('inf')
    current_layer_struct = [] # copy of the original 
    
    # print(f"The layers are {listify_layers}")
    
    if l_cutoff !=0:
        while (forgiveness_number != 0):
            # determine what a sweep is, and refactor this at the soonest
            # down sweep
            current_layer_struct = copy.deepcopy(best_layer_struct)
            for i in range(1, l_cutoff + 1): # [1, l_cutoff] is the real range
                # i are the indices of the free_layers in the downward sweep
                # print(f"At iter {i}, the bottom_nodes are {listify_layers[i]}")
                reordered_layer = sifting(current_layer_struct[i], current_layer_struct[i - 1], layerfy_edges[i])
                current_layer_struct[i] = reordered_layer
                # print(f"Downward sweep {i}, {listify_layers}")
                
            current_crossings = total_crossing_count_k_layer(current_layer_struct, edges)
            
            
            if current_crossings < min_crossings:
                min_crossings = current_crossings ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
                best_layer_struct = copy.deepcopy(current_layer_struct)
            else: # current >= min # did not improve or worse.
                forgiveness_number -= 1
                
            if forgiveness_number == 0: break
            
            # up sweep
            current_layer_struct = copy.deepcopy(best_layer_struct)
            for j in range(l_cutoff - 1, -1, -1): # [l_cutoff - 1, 0] is the real range
                # j should be the indices of the 'top_layer' that is the free_layer in upward sweep
                # print(f"At iter {j}, the free_nodes are {listify_layers[j]}")
                # print(f"Listify layer {j}:{listify_layers[j]}, {j+1}:{listify_layers[j+1]}, {layerfy_edges[j+1]}")
                reordered_layer = sifting(current_layer_struct[j], current_layer_struct[j + 1], layerfy_edges[j+1], 'upward')
                current_layer_struct[j] = reordered_layer
                # print(f"upward sweep {j}, {listify_layers}")
            
            current_crossings = total_crossing_count_k_layer(current_layer_struct, edges)
            
            if current_crossings < min_crossings:
                min_crossings = current_crossings   ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
                best_layer_struct = copy.deepcopy(current_layer_struct)
            else: # current >= min # did not improve or worse.
                forgiveness_number -= 1
                
            if forgiveness_number == 0: break
    
    #### barycenter one sweep
    if l_cutoff != (len(layers) - 1):
        for layer_idx in range(l_cutoff + 1, len(layers)):
            #l_cutoff+1 because we want all the 'lower' layers, len(edges) because max_idx+1=len(deges)
            formatted_edges = parse_edges(edges, best_layer_struct[layer_idx - 1], best_layer_struct[layer_idx])
            baryed_free_layer = barycenter(best_layer_struct[layer_idx], best_layer_struct[layer_idx - 1], formatted_edges)
            best_layer_struct[layer_idx] = baryed_free_layer
        
    return best_layer_struct