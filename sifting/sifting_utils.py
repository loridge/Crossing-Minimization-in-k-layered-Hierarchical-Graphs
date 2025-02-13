import sys, os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crossing_function.crossing_func import cross_count

def unzip_nodes():
    # TODO: implement hee
    pass



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
    
    # place the node to the leftmost position
    curr_lay_ord = current_layer_order[:best_position] + current_layer_order[best_position + 1: ] + [current_layer_order[best_position]]
    curr_crossing = float('inf') # set current crossing to very high number
    curr_position = len(curr_lay_ord) - 1
    
    # move to the leftmost while checking crossings and orderings
    for i in range(len(current_layer_order) - 1, -1, -1):
        # TODO: check crossings, update        
        curr_crossing = cross_count(fixed_layer_nodes, curr_lay_ord, pos, edges)
        
        # TODO: compare the crossing, update best position
        best_position = curr_position if curr_crossing < min_crossing else best_position
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
        curr_lay_ord = curr_lay_ord[: curr_position - 1] + [curr_lay_ord[curr_position]] + [curr_lay_ord[curr_position - 1]] + curr_lay_ord[curr_position + 1:]
    
    
    
    return best_layer_ord