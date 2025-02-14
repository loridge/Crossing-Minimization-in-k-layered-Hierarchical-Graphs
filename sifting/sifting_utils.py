import sys, os
import copy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crossing_function.crossing_func import cross_count

### for debugging purposes
import networkx as nx
import matplotlib.pyplot as plt
import json
###

def unzip_nodes():
    # TODO: implement hee
    pass

def adjust_pos_data(old_order: list[str], new_order: list[str], orig_pos: dict[str, list[float]]) -> dict[str, list[float]]:
    """Danger of manipulation of the dictionary, uses deepcopy due to Py not being pass by value or pass by ref.  

    Args:
        old_order (list[str]): _description_
        new_order (list[str]): _description_
        orig_pos (dict[str, list[float]]): _description_

    Returns:
        dict[str, list[float]]: _description_
    """
    set_coords = []
    dict_copy = copy.deepcopy(orig_pos)
    for node in old_order:
        # print(node, pos[node])
        set_coords.append(dict_copy[node])
        
    for node in new_order:
    # assign it to its corresponding set coords in the pos_copy
        dict_copy[node] = set_coords[new_order.index(node)]
    
    ## Generate a graph here for debugging
    nodes = [
    {"id": "u1", "depth": 1},
    {"id": "u2", "depth": 2},
    {"id": "u3", "depth": 2},
    {"id": "u4", "depth": 2},
    {"id": "u5", "depth": 1},
    {"id": "u6", "depth": 0},
    {"id": "u7", "depth": 0},
    {"id": "u8", "depth": 0}
]

    edges = [
    {"nodes": ["u1", "u7"]},
    {"nodes": ["u1", "u6"]},
    {"nodes": ["u1", "u8"]},
    {"nodes": ["u5", "u6"]},
    {"nodes": ["u5", "u7"]},
    {"nodes": ["u1", "u2"]},
    {"nodes": ["u1", "u3"]},
    {"nodes": ["u1", "u4"]},
    {"nodes": ["u5", "u3"]},
    {"nodes": ["u5", "u2"]}
    ]   
    
    # Create a graph
    G = nx.Graph()

    # Add nodes to the graph
    for node in nodes:
        G.add_node(node["id"], depth=node["depth"])  # Use 'layer' as 'depth'
        
    # Add edges to the graph, ensuring no same-layer edges
    # Also remove the edges that are same-layer
    new_edges = []
    for edge in edges:
        node1, node2 = edge["nodes"]
        if G.nodes[node1]["depth"] != G.nodes[node2]["depth"]:  # Check depths
            G.add_edge(node1, node2)
            # push the qualified edge to the new_edge array
            new_edges.append(edge)
        else: 
            pass
# Edges array should have now the qualified edges no same-layer edges
    
    plt.figure(figsize=(5, 3))
    nx.draw(
        G,
        pos=dict_copy,
        with_labels=True,
        node_size=2000,
        node_color="lightgreen",
        font_size=10,
        font_weight="bold",
        arrows=True,
    )

    # Display the graph
    plt.title("Graph with Multiple Layers and No Edges in Same Layer")
    plt.show()
    
    return dict_copy

def do_sifting(node_to_sift: str, current_layer_order: list, fixed_layer_nodes: list[str], pos, edges) -> list:
    """

    Args:
        node_to_sift (str): _description_
        current_layer_order (list): _description_
        fixed_layer_nodes (list): _description_
        pos (_type_): _description_

    Returns:
        list: list of nodes in their current order
    """
    
    # have the best position, best crossing, and best layer order be saved.
    best_position = current_layer_order.index(node_to_sift) # best position initialized to current position
    min_crossing = cross_count(fixed_layer_nodes, current_layer_order, pos, edges) # init minimum crossings
    best_layer_ord = current_layer_order
    best_pos_copy = copy.deepcopy(pos) # pos must be copied so that it can be altered in a way that will improve
    
    print(f"LOG: (INIT) do sifting; current node to be sifted: {node_to_sift}")
    print(f"LOG: (INIT) Inside do_sifting: best_position {best_position}, min crossing {min_crossing}, bestlayerord {best_layer_ord}")
    
    # place the node to the leftmost position, adjust pos_copy
    curr_lay_ord = current_layer_order[:best_position] + current_layer_order[best_position + 1: ] + [current_layer_order[best_position]]
    print(f"LOG-do_sifting-before sifting loop occurs curr_lay_ord should be at rightmost {curr_lay_ord}")
    curr_crossing = float('inf') # set current crossing to very high number
    print(f"LOG: showing the graph of {curr_lay_ord} INTRO")
    curr_pos_copy = adjust_pos_data(current_layer_order, curr_lay_ord, pos) # we adjust the graph coord data accdg to this new arrangement
    
    # move to the leftmost while checking crossings and orderings
    for i in range(len(current_layer_order) - 1, -1, -1):
        
        curr_position = i
        print(f"Curr position value {i}, free layer order to be checked: {curr_lay_ord}")
        curr_crossing = cross_count(fixed_layer_nodes, curr_lay_ord, curr_pos_copy, edges)
        # TODO: update the new_layer_ord
        if curr_crossing < min_crossing:
            best_position = curr_position
            best_layer_ord = curr_lay_ord   
            min_crossing = curr_crossing  
            best_pos_copy = curr_pos_copy ## watch out for deepcopying
            print(f"There was an update: best_position {best_position}, {best_layer_ord}, {min_crossing}")
            # how should we handle ties for different configurations?
            # TODO: handle ties, soon: CURRENT IMPLEMENTATION: crossings and best positions are not updated if curr_crossing is the same or greater.
        else:
            # do not update the best parameters
            pass
        
        # TODO: shift the node to the left, UPDATE curr_position, UPDATE curr_layer_ord
        # TODO: UPDATE pos_copy so that the cross_count function will work properly, and see the 'improvements'
        # BUG: check the logs, the curr_layer_ord just oscillates; ah due to the unupdated curr_position
        # BUG: no longer oscillates, but the behavior is unwanted!!!!
        prev_lay_ord = copy.deepcopy(curr_lay_ord)
        if (i != 0): 
            curr_lay_ord = curr_lay_ord[: curr_position - 1] + [curr_lay_ord[curr_position]] + [curr_lay_ord[curr_position - 1]] + curr_lay_ord[curr_position + 1:]   
        else: 
            pass # do nothing to that curr_lay_ord, lol!            
        print(f"LOG: inside do_sifting for loop; revised curr_lay_ord {curr_lay_ord} ")
        print(f"LOG: showing the graph of revised {curr_lay_ord}")
        curr_pos_copy = adjust_pos_data(prev_lay_ord, curr_lay_ord, curr_pos_copy)
        
    
    print(f"LOG: best_layer_ord of this run: {best_layer_ord}")
    return {"revised_lay_ord" : best_layer_ord, "revised_pos": best_pos_copy}