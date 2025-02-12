from typing import Dict, List

def node_neighbors(target: str, edges: list, fixed_layer_nodes: List[str]) -> list[str]:
    """
    Find all neighbors of a target node in a list of edges.

    This function takes a target node and a list of edges, and returns a list
    of all nodes that are directly connected to the target node.

    Args:
        target (str): The target node label.
        edges (list): A list of edges, where each edge is represented as a dictionary
                      with a "nodes" key containing a list of two node labels.
        fixed_layer_nodes (List[str]): The nodes in the fixed layer. Will be used for limiting the scope of the neighbors of a node in the free layer.
    Returns:
        list[str]: A list of node labels that are neighbors of the target node.
    """
    neighbors = []
    for edge_data in edges:
        edge_node_arr = edge_data["nodes"]
        if target in edge_node_arr:
            other_node = edge_node_arr[1] if edge_node_arr[0] == target else edge_node_arr[0]
            if other_node in fixed_layer_nodes:                
                neighbors.append(other_node)
    return neighbors


def u_prime_list_processor(target: str, pos: Dict[str, List[float]], free_layer: list) -> List[str]:
    """
    Finds all the nodes that are to the left of a target node in the same layer.
    Fills u_prime_nodes.

    Args:
        target (str): The target node label.
        pos (Dict[str, List[float]]): A dictionary containing the positional data of the nodes.
                                      The keys are node labels, and the values are lists of two floats
                                      representing the (x, y) coordinates of the nodes.
        free_layer: for now, it is an unordered list of the nodes in a layer that we are dealing with

    Returns:
        List[str]: A list of node labels that are to the left of the target node in the same layer.
    """
    target_coords = pos[target]
    u_prime_list = []

    # Trivial case where the target node is the only node in that layer is ignored
    # Case where there is nothing to the left is handled by the for loop
    # Case where there are at least 1 node to the left is handled by the for loop.
    if len(free_layer) != 1:
        for node in free_layer:
            if node == target:
                continue
            else:
                # if the x-coords of node is less than the x-coords of target node, push it to u_prime_list
                # NOTE: coords are usually used for graph drawing, technically u can implement this using an ordered list
                # we have to check pos because we know that the given layers might be unordered according to how pos orders them to.
                ### we have no assurances, we might no longer need pos if sure na yung list is randomly ordered 
                if pos[node][0] < target_coords[0]:
                    u_prime_list.append(node)

    return u_prime_list

def u_prime_neighbor_filter(target_u_prime: str, u_neighbor: str, edges: list, fixed_layer_nodes: List[str], pos) -> List[str]:
    """
    For a certain node u_prime, we filter its neighbors (list of v_primes that are in fixed layer) that satisfies v_prime > v.
    v in this case is the u_neighbor.
    
    Args:
        target_u_prime (str): The node u_prime in which we will find its neighboring nodes
        u_neighbor (str): A neighbor node of u node where the x-coords of u_prime_neighbors will be compared.
        edges (list[str]): List of edges. 
        fixed_layer_nodes (List[str]): The nodes in the fixed layer. Will be used for limiting the scope of the neighbors of a node in the free layer.
        pos (Dict[str, List[float]]): A dictionary containing the positional data of the nodes.
                                      The keys are node labels, and the values are lists of two floats
                                      representing the (x, y) coordinates of the nodes.
    
    """ 
    u_prime_neighbors = node_neighbors(target_u_prime, edges, fixed_layer_nodes)
    filtered_u_prime_neighbors = []
    for v_prime in u_prime_neighbors:
        v_prime_coords = pos[v_prime]
        u_neighbor_coords = pos[u_neighbor]
        
        if v_prime_coords[0] > u_neighbor_coords[0]:
            filtered_u_prime_neighbors.append(v_prime)
    
    return filtered_u_prime_neighbors