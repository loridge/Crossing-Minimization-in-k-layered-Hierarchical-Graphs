import sys, os
import copy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crossing_function.crossing_func import cross_count

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
    
    print(f"LOG: do sifting; current node to be sifted: {node_to_sift}")
    print(f"LOG: Inside do_sifting: best_position {best_position}, min crossing {min_crossing}, bestlayerord {best_layer_ord}")
    
    # place the node to the leftmost position, adjust pos_copy
    curr_lay_ord = current_layer_order[:best_position] + current_layer_order[best_position + 1: ] + [current_layer_order[best_position]]
    curr_crossing = float('inf') # set current crossing to very high number
    curr_pos_copy = adjust_pos_data(current_layer_order, curr_lay_ord, pos)
    
    print(f"LOG-do_sifting-before sifting loop occurs curr_lay_ord should be at rightmost {curr_lay_ord}")
    
    # move to the leftmost while checking crossings and orderings
    for i in range(len(current_layer_order) - 1, -1, -1):
        print("Curr position value", i)
        # TODO: check crossings,    
        curr_crossing = cross_count(fixed_layer_nodes, curr_lay_ord, curr_pos_copy, edges)
        curr_position = i
        # TODO: update the new_layer_ord
        if curr_crossing < min_crossing:
            best_position = curr_position
            best_layer_ord = curr_lay_ord   
            min_crossing = curr_crossing         
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
        curr_lay_ord = curr_lay_ord[: curr_position - 1] + [curr_lay_ord[curr_position]] + [curr_lay_ord[curr_position - 1]] + curr_lay_ord[curr_position + 1:]
        print(f"LOG: inside do_sifting for loop; curr_lay_ord {curr_lay_ord} ")
        curr_pos_copy = adjust_pos_data(prev_lay_ord, curr_lay_ord, pos)
        
    
    
    return best_layer_ord