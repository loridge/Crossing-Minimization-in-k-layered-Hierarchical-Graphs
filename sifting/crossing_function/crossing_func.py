from .crossing_utils import node_neighbors, u_prime_neighbor_filter, u_prime_list_processor

# Crossing function or Objective Function
def cross_count(fixed_layer: list[str], free_layer: list[str], edges: list, ) -> int:
    """
    Calculate the number of edge crossings between two layers in a bipartite graph.

    This function counts all of the crossings present in a bipartite graph. The function takes two lists of node labels representing 
    two layers of the graph and the positional data of the nodes in the Cartesian plane. U is free, L is fixed. 
    node u belongs to free_layer. node v belongs to fixed_layer.
    
    Args:        
        fixed_layer (list[str]): List of node labels in the fixed layer. e.g. ["u2", "u3", "u4"]
        free_layer (list[str]): List of node labels in the free layer. e.g. ["u2", "u3", "u4"]
        pos_data (dict): Dictionary containing the positional data of the nodes.
                         The keys are node labels, and the values are (x, y) tuples
                         representing the positions of the nodes.
        edges (list): List of edges in the graph.

    Returns:
        int: The total number of edge crossings between the two layers.
    """
    # Reference: https://studenttheses.uu.nl/bitstream/handle/20.500.12932/46720/final_Bachelor_Thesis_Mathematics.pdf?sequence=1&isAllowed=y
    crossing_total = 0
    
    fixed_layer = [f"u{node}" if isinstance(node, int) else node for node in list(fixed_layer) ]
    free_layer =  [f"u{node}" if isinstance(node, int) else node for node in list(free_layer) ]
    
    total_neighbors = 0
    for u_node in free_layer:
        neighbor_u_node = []
        # TODO: implement filling of neighbor_u_node
        neighbor_u_node = node_neighbors(u_node, edges, fixed_layer)
        total_neighbors += len(neighbor_u_node)
        # print("neighbor u  node", neighbor_u_node)
        for v_node in neighbor_u_node:
            u_prime_nodes = []
            # TODO: implement filling u_prime, list of node u that are positioned to the left of u
            u_prime_nodes = u_prime_list_processor(u_node, free_layer)
            for u_prime in u_prime_nodes:
                # TODO: implement filtering of nodes 
                result = []                
                result = u_prime_neighbor_filter(u_prime, v_node, edges, fixed_layer)
                crossing_total += len(result)

    return crossing_total



def binary_search_first_smaller(arr, v, lower_bound, upper_bound, index_references, v_index):
    """
    Binary search to find the rightmost index in 'arr' where the value is smaller than 'v'.
    The search starts from 'lower_bound' and ends at 'upper_bound' to optimize performance.

    Args:
        arr (list[str]): The sorted list of neighbor nodes.
        v (str): The node to compare against.
        lower_bound (int): The starting index for the search.
        upper_bound (int): The ending index for the search.
        index_references (dict): Dictionary mapping nodes to their fixed_layer indices.
        v_index (int): The index of the node 'v' in the fixed layer.

    Returns:
        int: The index of the last element smaller than 'v', or -1 if none exist.
    """
    left, right = lower_bound, upper_bound
    result = -1  # Default to -1 (not found)

    while left <= right:  # Fix condition to include rightmost element
        mid = (left + right) // 2
        # print(f"DEBUG INSIDE BINSEARCH arr[mid]: {arr[mid]}, left: {left}, right: {right}, mid: {mid}")

        if index_references[arr[mid]] < v_index:
            result = mid  # Update result, but keep searching to the right
            left = mid + 1
        else:
            right = mid - 1  # Move left to find a smaller value

    return result  # Final rightmost valid index


def cross_count_optimized(fixed_layer: list[str], free_layer: list[str], edges: list):
    """Implements the crossing function made by Simon Hol (2024)

    Args:
        fixed_layer (list[str]): _description_
        free_layer (list[str]): _description_
        edges (list): Array of {'nodes':[node1:str, node2:str]} objects
    Returns:
        _type_: _description_
    """
    crossing_total = 0
    
    fixed_layer = [f"u{node}" if isinstance(node, int) else node for node in list(fixed_layer) ]
    free_layer =  [f"u{node}" if isinstance(node, int) else node for node in list(free_layer) ]

    fixed_layer_dict = {node: index for index, node in enumerate(fixed_layer)}
    free_layer_dict = {node: index for index, node in enumerate(free_layer)}

    neighbor_dict = {node: [] for node in free_layer}
    easy_free = set(free_layer)
    easy_fixed = set(fixed_layer)

    for edge_data in edges:
        u, v = edge_data["nodes"]
        if u in easy_free and v in easy_fixed:
            neighbor_dict[u].append(v)
        elif v in easy_free and u in easy_fixed:
            neighbor_dict[v].append(u)

    # Sort neighbors based on their position in fixed_layer
    for node in neighbor_dict:
        neighbor_dict[node].sort(key=lambda x: fixed_layer_dict[x])
    # print(f"free{free_layer}, fixed{fixed_layer}")
    # print("DEBUG NEIGHBOR DICT ,",neighbor_dict) #####################################################################################################
    # print("DEBUG: free layer dict", free_layer_dict)
    # print("DEBUG: fixed layer dict", fixed_layer_dict)
    #### CROSSING PROPER ####
    for i, u_node in enumerate(free_layer):
        u_neighbors = neighbor_dict[u_node]
        u_prime_nodes = free_layer[i + 1:]
        # print("")
        # print("u_node ", u_node, ";;;u_prime nodes > u_node: ",u_prime_nodes)
        for u_prime in u_prime_nodes:
          u_prime_neighbors = neighbor_dict[u_prime]
          lb = 0   # 0 indexed as opposed to pseudocode
          ub = len(u_prime_neighbors) - 1  # 0 indexed as opposed to pseudocode
          # print(f"DEBUG u-prime-neighbors: {u_prime_neighbors} of u-prime {u_prime}")
          for v in u_neighbors:
              result = binary_search_first_smaller(u_prime_neighbors, v, lb, ub, fixed_layer_dict, fixed_layer_dict[v]) ##, edit it must be based on indices not the values of the elements themselves
              # print(f"DEBUG result u-node -{u_node}: {result} of v {v} for u-prime-neigh {u_prime_neighbors} of u-prime{u_prime}")
              # lb = result + 1 # result minus 1 because pls see the binary search implementation
              if result != -1:
                crossing_total += result + 1

    return crossing_total
