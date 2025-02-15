from crossing_function.crossing_utils import node_neighbors, u_prime_neighbor_filter, u_prime_list_processor

# Crossing function or Objective Function
def cross_count(fixed_layer: list[str], free_layer: list[str], pos_data: dict, edges: list, layered_pos_data=None) -> int:
    """
    Calculate the number of edge crossings between two layers in a bipartite graph.

    This function counts all of the crossings present in a bipartite graph. The function takes two lists of node labels representing 
    two layers of the graph and the positional data of the nodes in the Cartesian plane. U is free, L is fixed. 
    node u belongs to free_layer. node v belongs to fixed_layer.
    
    Args:        
        fixed_layer (list[str]): List of node labels in the fixed layer.
        free_layer (list[str]): List of node labels in the free layer.
        pos_data (dict): Dictionary containing the positional data of the nodes.
                         The keys are node labels, and the values are (x, y) tuples
                         representing the positions of the nodes.
        edges (list): List of edges in the graph.
        layered_pos_data (dict, optional): Dictionary containing the layered positional data of the nodes.
                                           Defaults to None.

    Returns:
        int: The total number of edge crossings between the two layers.
    """
    # Reference: https://studenttheses.uu.nl/bitstream/handle/20.500.12932/46720/final_Bachelor_Thesis_Mathematics.pdf?sequence=1&isAllowed=y
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