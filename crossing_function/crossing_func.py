from crossing_function.crossing_utils import node_neighbors, u_prime_neighbor_filter, u_prime_list_processor

# Crossing function or Objective Function
def cross_count(fixed_layer: list[str], free_layer: list[str], pos_data: dict, edges: list, layered_pos_data=None) -> int:
    """_summary_

    Args:
        fixed_layer (list[str]): _description_
        free_layer (list[str]): _description_
        pos_data (dict): _description_
        edges (list): _description_
        layered_pos_data (_type_, optional): _description_. Defaults to None.

    Returns:
        int: _description_
    """
    crossing_total = 0
    
    for u_node in free_layer:
        neighbor_u_node = []
        # TODO: implement filling of neighbor_u_node
        neighbor_u_node = node_neighbors(u_node, edges, fixed_layer)
        for v_node in neighbor_u_node:
            u_prime_nodes = []
            # TODO: implement filling u_prime, list of node u that are positioned to the left of u
            u_prime_nodes = u_prime_list_processor(u_node, pos_data, free_layer)
            for u_prime in u_prime_nodes:
                # TODO: implement filtering of nodes 
                result = []                
                result = u_prime_neighbor_filter(u_prime, v_node, edges, fixed_layer, pos_data)

                crossing_total += len(result)
                
    return crossing_total