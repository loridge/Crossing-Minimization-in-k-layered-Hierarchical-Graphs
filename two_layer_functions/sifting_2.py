import sys, os
from typing import Union, List, Set
# import bisect 
# import copy

from .crossing_utils import node_neighbors
from .crossing_func import cross_count, cross_count_optimized
from .sifting_util2 import do_sifting
# Sifting function
def sifting_2(free_layer: list[str], fixed_layer: list[str], edges: list, verbose=0,) -> list:
    """
    [OLD DESCRIPTION]
    Perform the sifting algorithm to reorder the free layer nodes to minimize edge crossings.

    This function reorders the nodes in the free layer based on their indegree and positional data
    to minimize the number of edge crossings in the graph. The output is the new graph positioning
    and the reordered free layer.

    Args:
        free_layer (list[str]): List of node labels in the free layer. The "bottom nodes".
        fixed_layer (list[str]): List of node labels in the fixed layer.
        edges (list): List of edges in the graph.
        pos (dict): Dictionary containing the positional data of the nodes.
                    The keys are node labels, and the values are (x, y) tuples
                    representing the positions of the nodes.
        verbose (int, optional): Verbosity level for debugging output. Defaults to 0.
        
    Returns:
        list: A list of reordered free layer nodes <new implementation>
    """   
        # dict: A dictionary containing the new graph positioning and the reordered free layer.
        #       The keys are:
        #         - "sifting_layer_ord": The reordered free layer node labels.
        #         - "sifting_pos": The new positional data of the nodes.
    
    
    
    # Make a PRIORITY QUEUE for nodes in descending order of their indegrees.
    ## element format (node, indegree)    
    
    indeg_prio_queue = []
    
    for node in free_layer:
        indeg_cnt = len(node_neighbors(node, edges, fixed_layer))
        indeg_prio_queue.append((node, indeg_cnt))
        
    sorted_indeg_prio_queue = [item for item, _ in sorted(indeg_prio_queue, key=lambda x: x[1], reverse=True)] # ditching the indegree values after the sorting has been done
    if verbose: print("sorted_indeg_prio_queue", sorted_indeg_prio_queue)
    
    current_layer_order = free_layer[:] # assumed that free_layer order is already ordered in a sense.
    
    for node in sorted_indeg_prio_queue:
        if verbose:
            print(f"-----------New Run with the node to be sifted: {node} ---------")
            print(f"This is the current layer order func-sifting: {current_layer_order}")
        result = do_sifting(node, current_layer_order, fixed_layer, edges, verbose=verbose)
        current_layer_order = result["revised_lay_ord"]
        
    if verbose:
        print("---------------------------")
        print(f"FINAL CURRENT LAYER ORDER {current_layer_order}")
    
    # return new graph coords and the new order 
    # return {"sifting_layer_ord": current_layer_order,}
    return current_layer_order


def sifting_inactivated(free_layer: Union[Set[str], List[str]], fixed_layer: Union[Set[str], List[str]], edges: list, verbose=0,) -> list:
    """
    Perform the sifting algorithm to reorder the free layer nodes to minimize edge crossings.

    Args:
        free_layer (Union[Set[str], List[str]]): Set or list of node labels in the free layer.
        fixed_layer (Union[Set[str], List[str]]): Set or list of node labels in the fixed layer.
        edges (list): List of edges in the graph.
        verbose (int, optional): Verbosity level for debugging output. Defaults to 0.
        generated (int, optional): 0 if from the RomeLibDataset, 1 if from a generated bipartite graph made by LA. This will make the function handle things differently.

    Returns:
        list: A list of reordered free layer nodes.
    """
    # wrapper para compatible haha 
    
    fixed_layer = [f"u{node}" if isinstance(node, int) else node for node in list(fixed_layer) ]
    free_layer =  [f"u{node}" if isinstance(node, int) else node for node in list(free_layer) ]   
    
    reordered_layer = sifting_2(free_layer, fixed_layer, edges, verbose)
    
    try: 
        reordered_layer = [int(node[1:]) if isinstance(node, str) and node.startswith('u') and node[1:].isdigit() else node for node in reordered_layer]    
    except:
        print("ERROR: fixed layer =>", fixed_layer)
        print("ERROR: free layer =>", free_layer)
        
        print("ERROR: Reordered layer =>", reordered_layer)
    return reordered_layer


def sifting(free_nodes, fixed_nodes, edges, sweep_type='downward'):
    """
    Reorders bottom nodes using the sifting heuristic based on indegree in decreasing order.
    
    Parameters:
    - bottom_nodes: List of bottom-layer nodes.
    - top_nodes: List of top-layer nodes.
    - edges: List of dictionaries representing edges with format {'nodes': ['uX', 'uY']}.
    - sweep_type[str]: 'downward' if downward sweep, 'upward' if upward sweep. Defaults to downward.
    Returns:
    - Reordered list of bottom-layer nodes as integers.
    """
    
    fixed_nodes = [f"u{node}" if isinstance(node, int) else node for node in list(fixed_nodes) ]
    free_nodes = [f"u{node}" if isinstance(node, int) else node for node in list(free_nodes) ]  
    
    # Compute indegree for each bottom node (sa obcm lang), free layer sya sa k-layer
    indegree = {node: 0 for node in free_nodes}
    for edge in edges: ##########################################MAY BUG PAG UPWARD SWEEP
        if sweep_type == 'downward':
            _, b = edge['nodes'] # this only works for obcm where there is a clear bottom node
        elif sweep_type == 'upward':
            b, _ = edge['nodes']
        indegree[b] += 1
    
    # Sort bottom nodes by indegree in decreasing order (priority queue for processing order)
    sorted_nodes = sorted(free_nodes, key=lambda node: -indegree[node])
    
    # Apply the sifting heuristic
    for node in sorted_nodes:
        best_position = free_nodes.index(node)
        best_crossings = cross_count_optimized(fixed_nodes, free_nodes, edges)
        
        for j in range(len(free_nodes)):
            if free_nodes[j] == node:
                continue
            
            # Swap node to new position
            free_nodes.remove(node)
            free_nodes.insert(j, node)
            current_crossings = cross_count_optimized(fixed_nodes, free_nodes, edges)
            
            if current_crossings < best_crossings:
                best_position = j
                best_crossings = current_crossings
            
            # Revert swap
            free_nodes.remove(node)
            free_nodes.insert(best_position, node)
    
    # Extract integer values from node labels
    return [int(node[1:]) if isinstance(node, str) and node.startswith('u') and node[1:].isdigit() else node for node in free_nodes]