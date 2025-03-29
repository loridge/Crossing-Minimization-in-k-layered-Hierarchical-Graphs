import sys, os
from itertools import permutations
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)
from sifting.crossing_function.crossing_func import cross_count

def minimize_crossings(fixed_layer, free_layer, edges):
    """
    Find the optimal ordering of the free layer to minimize edge crossings.
    
    Parameters:
    - fixed_layer: List of vertices in the fixed layer (fixed order).
    - free_layer: List of vertices in the free layer.
    - edges: List of dictionaries with 'nodes' key, each containing a list of two vertices representing an edge.
    
    Returns:
    - Optimal ordering of free_layer with minimal crossings.
    - Minimum number of crossings.
    """
    min_crossings = float('inf')
    optimal_ordering = None
    
    # Generate all possible permutations of the free layer
    for perm in permutations(free_layer):
        # Calculate the number of crossings for the current permutation
        current_crossings = cross_count(fixed_layer, list(perm), edges)
        
        # Update the optimal ordering if the current permutation has fewer crossings
        if current_crossings < min_crossings:
            min_crossings = current_crossings
            optimal_ordering = perm
    
    return list(optimal_ordering), min_crossings

# Example usage:
fixed_layer = ['u1', 'u2', 'u3']
free_layer = ['u4', 'u5', 'u6']
edges = [
    {'nodes': ['u1', 'u4']},
    {'nodes': ['u2', 'u5']},
    {'nodes': ['u3', 'u6']},
    {'nodes': ['u1', 'u6']},
    {'nodes': ['u2', 'u4']}
]

optimal_order, min_cross = minimize_crossings(fixed_layer, free_layer, edges)
print("Optimal Ordering of Free Layer:", optimal_order)
print("Minimum Number of Crossings:", min_cross)
