import sys, os
import bisect 
import copy

from sifting.archive.sifting_utils import do_sifting
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crossing_function.crossing_utils import node_neighbors

# Sifting function
def sifting(free_layer: list[str], fixed_layer: list[str], edges: list, pos, verbose=0) -> dict:
    """
    Perform the sifting algorithm to reorder the free layer nodes to minimize edge crossings.

    This function reorders the nodes in the free layer based on their indegree and positional data
    to minimize the number of edge crossings in the graph. The output is the new graph positioning
    and the reordered free layer.

    Args:
        free_layer (list[str]): List of node labels in the free layer.
        fixed_layer (list[str]): List of node labels in the fixed layer.
        edges (list): List of edges in the graph.
        pos (dict): Dictionary containing the positional data of the nodes.
                    The keys are node labels, and the values are (x, y) tuples
                    representing the positions of the nodes.
        verbose (int, optional): Verbosity level for debugging output. Defaults to 0.

    Returns:
        dict: A dictionary containing the new graph positioning and the reordered free layer.
              The keys are:
                - "sifting_layer_ord": The reordered free layer node labels.
                - "sifting_pos": The new positional data of the nodes.
    """   
    
    # Make a PRIORITY QUEUE for nodes in descending order of their indegrees.
    ## element format (node, indegree)    
    indeg_prio_queue = []
    
    for node in free_layer:
        indeg_cnt = len(node_neighbors(node, edges, fixed_layer))
        indeg_prio_queue.append((node, indeg_cnt))
        
    sorted_indeg_prio_queue = [item for item, _ in sorted(indeg_prio_queue, key=lambda x: x[1], reverse=True)] # ditching the indegree values after the sorting has been done
    if verbose: print("sorted_indeg_prio_queue", sorted_indeg_prio_queue)
    
    # TODO: use the pos to rearrange free_layer, since original free_layer only contains the nodes needed, not the order
    current_layer_order = [] 

    for node in free_layer:
        x_coord = pos[node][0]
        node_info = (node, x_coord)
        bisect.insort(current_layer_order, node_info)   
    
    # now we assume that the order of current_layer_order is based on the order as stated in pos and not in the ordering seen in free_layer list

    current_layer_order=[node for node, _ in current_layer_order]
    current_pos_data = copy.deepcopy(pos)
    for node in sorted_indeg_prio_queue:
        if verbose:
            print(f"-----------New Run with the node to be sifted: {node} ---------")
            print(f"This is the current layer order func-sifting: {current_layer_order}")
        result = do_sifting(node, current_layer_order, fixed_layer, current_pos_data, edges, verbose=verbose)
        current_layer_order = result["revised_lay_ord"]
        current_pos_data = result["revised_pos"]
    if verbose:
        print("---------------------------")
        print(f"FINAL CURRENT LAYER ORDER {current_layer_order}")
    # X-COORD PROBLEM
    # pag sinift mo ba, pano mag-aadjust x-coords?? how will it be recomputed?
    # the crossing function only uses the positions, but let us check how this will work if only the node are given
    # barycenter explicity uses it, but for sifting??
    ## does it preserve the original x-coords na parang slots na iinsert mo doon, or magbabago x-coords
    
    
    # return new graph coords and the new order 
    return {"sifting_layer_ord": current_layer_order, "sifting_pos": current_pos_data}