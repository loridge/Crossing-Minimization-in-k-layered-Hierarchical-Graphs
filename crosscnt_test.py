from typing import Dict, List
from crossing_utils import node_neighbors


# Example usage
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

layered_pos = {1: ['u1', 'u5'], 2: ['u2', 'u3', 'u4'], 0: ['u6', 'u7', 'u8']}
pos = {
    "u1": [-0.5, -2],
    "u5": [0.5, -2],
    "u2": [-1.0, -4],
    "u3": [0.0, -4],
    "u4": [1.0, -4],
    "u6": [-1.0, 0],
    "u7": [0.0, 0],
    "u8": [1.0, 0]
}

target = "u7"
def u_prime_neighbor_filter(target_u_prime: str, u_neighbor: str, edges: list, pos) -> List[str]:
    """
    For a certain node u_prime, we filter its neighbors (list of v_primes) that satisfies v_prime > v.
    v in this case is the u_neighbor.
    
    Args:
        target_u_prime (str): The node u_prime in which we will find its neighboring nodes
        u_neighbor (str): A neighbor node of u node where the x-coords of u_prime_neighbors will be compared.
        edges (list[str]): List of edges 
        pos (Dict[str, List[float]]): A dictionary containing the positional data of the nodes.
                                      The keys are node labels, and the values are lists of two floats
                                      representing the (x, y) coordinates of the nodes.
    
    """ 
    u_prime_neighbors = node_neighbors(target_u_prime, edges)
    filtered_u_prime_neighbors = []
    for v_prime in u_prime_neighbors:
        v_prime_coords = pos[v_prime]
        u_neighbor_coords = pos[u_neighbor]
        
        if v_prime_coords[0] > u_neighbor_coords[0]:
            filtered_u_prime_neighbors.append(v_prime)
    
    return filtered_u_prime_neighbors
    
a = u_prime_neighbor_filter("u6", "u1", edges, pos)
print(a)