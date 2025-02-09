def node_neighbors(target: str, edges: list) -> list[str]:
    """
    Find all neighbors of a target node in a list of edges.

    This function takes a target node and a list of edges, and returns a list
    of all nodes that are directly connected to the target node.

    Args:
        target (str): The target node label.
        edges (list): A list of edges, where each edge is represented as a dictionary
                      with a "nodes" key containing a list of two node labels.

    Returns:
        list[str]: A list of node labels that are neighbors of the target node.
    """
    neighbors = []
    for edge_data in edges:
        edge_node_arr = edge_data["nodes"]
        if target in edge_node_arr:
            other_node = edge_node_arr[1] if edge_node_arr[0] == target else edge_node_arr[0]
            neighbors.append(other_node)
    return neighbors