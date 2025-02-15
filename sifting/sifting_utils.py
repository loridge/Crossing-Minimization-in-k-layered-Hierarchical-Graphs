import sys, os
import copy

### for debugging purposes
import networkx as nx
import matplotlib.pyplot as plt
import json
###

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crossing_function.crossing_func import cross_count

def adjust_pos_data(old_order: list[str], new_order: list[str], orig_pos: dict[str, list[float]], demo=0) -> dict[str, list[float]]:
    """Changes positional coordinate data by the new order of nodes in a layer. Uses copy.deepcopy due to Py not being pass by value or pass by ref that leads to the manipulation of the original pos object.  

    Args:
        old_order (list[str]): The previous ordering of the nodes of a layer.
        new_order (list[str]): The adjusted ordering of the nodes of a layer.
        orig_pos (dict[str, list[float]]): The previous state of the pos object. 
        demo (int): WIP - Toggle the display of a visualizer that shows the current state of the graph when this function is called. 
    Returns:
        dict[str,list[float]]: A new state of the pos object.
    """
    set_coords = []
    dict_copy = copy.deepcopy(orig_pos)
    for node in old_order:
        if demo: print(node, orig_pos[node])
        set_coords.append(dict_copy[node])
        
    for node in new_order:
        dict_copy[node] = set_coords[new_order.index(node)] # assign it to its corresponding set coords in the pos_copy
    
    # TODO: implement that it uses the passed data. Might need nodes and edge data
    if demo == 1:        
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

def do_sifting(node_to_sift: str, current_layer_order: list, fixed_layer_nodes: list[str], pos, edges, verbose=0) -> list:
    """
    Perform the sifting algorithm for a single node to minimize edge crossings.

    This function repositions a single node within its layer to minimize the number of edge crossings
    in the graph. It iteratively moves the node to different positions and calculates the number of
    crossings, keeping track of the best position with the fewest crossings.

    Args:
        node_to_sift (str): The label of the node to be sifted.
        current_layer_order (list[str]): The current order of nodes in the free layer.
        fixed_layer_nodes (list[str]): The list of node labels in the fixed layer.
        pos (dict): Dictionary containing the positional data of the nodes.
                    The keys are node labels, and the values are (x, y) tuples
                    representing the positions of the nodes.
        edges (list): List of edges in the graph.
        verbose (int, optional): Verbosity level for debugging output. Defaults to 0.

    Returns:
        dict: A dictionary containing the revised layer order and the revised positional data.
              The keys are:
                - "revised_lay_ord": The revised order of nodes in the free layer.
                - "revised_pos": The revised positional data of the nodes.
    """
    
    # have the best position, best crossing, and best layer order be saved.
    best_position = current_layer_order.index(node_to_sift) # best position initialized to current position
    min_crossing = cross_count(fixed_layer_nodes, current_layer_order, pos, edges) # init minimum crossings
    best_layer_ord = current_layer_order
    best_pos_copy = copy.deepcopy(pos) # pos must be copied so that it can be altered in a way that will improve
    
    if verbose == 1:
        print(f"LOG: (INIT) do sifting; current node to be sifted: {node_to_sift}")
        print(f"LOG: (INIT) Inside do_sifting: best_position {best_position}, min crossing {min_crossing}, bestlayerord {best_layer_ord}")
    
    # place the node to the leftmost position, adjust pos_copy
    curr_lay_ord = current_layer_order[:best_position] + current_layer_order[best_position + 1: ] + [current_layer_order[best_position]]
    if verbose: print(f"LOG-do_sifting-before sifting loop occurs curr_lay_ord, node should be at rightmost {curr_lay_ord}")
    curr_crossing = float('inf') # set current crossing to very high number
    if verbose: print(f"LOG: (INTRO) showing the graph of {curr_lay_ord}")
    curr_pos_copy = adjust_pos_data(current_layer_order, curr_lay_ord, pos) # we adjust the graph coord data accdg to this new arrangement
    
    # move the node to the leftmost while checking crossings and orderings
    for i in range(len(current_layer_order) - 1, -1, -1):
        curr_position = i
        if verbose: print(f"Curr position value {i}, free layer order to be checked: {curr_lay_ord}")
        curr_crossing = cross_count(fixed_layer_nodes, curr_lay_ord, curr_pos_copy, edges)
        # TODO: update the new_layer_ord
        if curr_crossing < min_crossing:
            best_position = curr_position
            best_layer_ord = curr_lay_ord   
            min_crossing = curr_crossing  
            best_pos_copy = curr_pos_copy ## watch out for deepcopying
            if verbose: print(f"\033[32mThere was an update: best_position {best_position}, best_lay_ord {best_layer_ord}, min_xsing {min_crossing}\033[30m")
            # how should we handle ties for different configurations?
            # TODO: handle ties, soon: CURRENT IMPLEMENTATION: crossings and best positions are not updated if curr_crossing is the same or greater.
        else:
            # do not update the best parameters
            pass
        
        prev_lay_ord = copy.deepcopy(curr_lay_ord)
        if (i != 0): 
            curr_lay_ord = curr_lay_ord[: curr_position - 1] + [curr_lay_ord[curr_position]] + [curr_lay_ord[curr_position - 1]] + curr_lay_ord[curr_position + 1:]   
        else: 
            pass # do nothing to curr_lay_ord. 
        
        if verbose:        
            print(f"LOG: inside do_sifting for loop; revised curr_lay_ord {curr_lay_ord} ")
            print(f"LOG: showing the graph of revised {curr_lay_ord}")
        curr_pos_copy = adjust_pos_data(prev_lay_ord, curr_lay_ord, curr_pos_copy)
        
    
    if verbose: print(f"\033[35mLOG: best_layer_ord of this run: {best_layer_ord}\n\033[30m")
    return {"revised_lay_ord" : best_layer_ord, "revised_pos": best_pos_copy}