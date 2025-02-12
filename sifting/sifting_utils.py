import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crossing_function.crossing_func import cross_count

def unzip_nodes():
    # TODO: implement hee
    pass



def do_sifting(node_to_sift: str, current_layer_order: list, fixed_layer_nodes: list, pos, edges) -> list:
    """

    Args:
        node_to_sift (str): _description_
        current_layer_order (list): _description_
        fixed_layer_nodes (list): _description_
        pos (_type_): _description_

    Returns:
        list: list of nodes in their current order
    """
    
    # current_layer_order is correct    
    
    best_position = current_layer_order.index(node_to_sift) # best position initialized to current position
    
    min_crossings = cross_count(fixed_layer_nodes, current_layer_order, pos, edges) # init minimum crossings
    
    # place the node to the leftmost position
    curr_lay_ord = current_layer_order[:best_position] + current_layer_order[best_position + 1: ] + [current_layer_order[best_position]]
    best_position = len(current_layer_order) - 1
    
    # new layer order
    new_layer_ord = []
    
    # move to the leftmost while checking crossings and orderings
    for i in range(len(current_layer_order) - 1, -1, -1):
        
        print("placeholder", i)

    
    
    
    return new_layer_ord