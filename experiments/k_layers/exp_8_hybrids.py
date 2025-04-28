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
    permutation_patarasuk,
)

from k_layered import (
    generate_k_layered_sparse_graph,
    visualize_k_layered_graph,
)

from k_layer_crossing import (
    total_crossing_count_k_layer,
)


def parse_layers_edges(layers, edges)->dict:
    """Multiple algorithms just use the same preprocessing inside.

    Args:
        layers (_type_): _description_
        edges (_type_): _description_

    Returns:
        dict: _description_
    """
    k = len(layers)
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
    
    return {'listify_layers':  listify_layers, 'layerfy_edges': layerfy_edges}
    pass

def bary_sifting(layers, edges: list[list], l_cutoff, parsed_layer_edges) -> list[list]:
    """Made for Experiment 8, this is a reoptimization algorithm that uses barycenter and sifting for k-layered crossing minimization. 

    Args:
        layers (_type_): _description_
        edges (list[list]): _description_
        l_cutoff (_type_): _description_

    Returns:
        list[list]: _description_
    """
    
    if (0 <= l_cutoff <= (len(layers) - 1)) is False:
        print(f"Invalid l_cutoff value, it must be from 1 to {len(layers) - 1}")
        exit(0)
        
    forgiveness_number = 20
    k = len(layers)
    
   
    
    
    pass