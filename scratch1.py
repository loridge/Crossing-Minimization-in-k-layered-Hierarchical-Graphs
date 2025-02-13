import networkx as nx
import matplotlib.pyplot as plt
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crossing_function.crossing_func import cross_count
from crossing_function.crossing_utils import node_neighbors
import bisect 
import itertools
import copy
nodes = [
    {"id": "u1", "depth": 1},
    {"id": "u2", "depth": 2},
    {"id": "u3", "depth": 2},
    {"id": "u4", "depth": 2},
    {"id": "u5", "depth": 1},
    {"id": "u6", "depth": 0},
    {"id": "u7", "depth": 0},
    {"id": "u8", "depth": 0}
]

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

# Create a graph
G = nx.Graph()

# Add nodes to the graph
for node in nodes:
    G.add_node(node["id"], depth=node["depth"])  # Use 'layer' as 'depth'
    
# Add edges to the graph, ensuring no same-layer edges
# Also remove the edges that are same-layer
new_edges = []
for edge in edges:
    node1, node2 = edge["nodes"]
    if G.nodes[node1]["depth"] != G.nodes[node2]["depth"]:  # Check depths
        G.add_edge(node1, node2)
        # push the qualified edge to the new_edge array
        new_edges.append(edge)
    else: 
        pass
# Edges array should have now the qualified edges no same-layer edges
edges = new_edges

# Initialize positions for nodes grouped by depths
layered_pos = {}
for node in G.nodes():
    depth = G.nodes[node]["depth"]
    if depth not in layered_pos:
        layered_pos[depth] = []
    layered_pos[depth].append(node)

pos = {}
layer_height = 2  # Vertical spacing between layers
for layer, nodes_in_layer in layered_pos.items():
    # Sort nodes in each layer by their 'id' in increasing order
    nodes_in_layer.sort()  # Sort alphabetically by id
    x_offset = -(len(nodes_in_layer) - 1) / 2  # Center nodes horizontally
    for i, node in enumerate(nodes_in_layer):
        pos[node] = (x_offset + i, -layer * layer_height)

        
pos_silenced = {
    "u1": [
        -0.5,
        -2
    ],
    "u5": [
        0.5,
        -2
    ],
    "u2": [
        -1.0,
        -4
    ],
    "u3": [
        0.0,
        -4
    ],
    "u4": [
        1.0,
        -4
    ],
    "u6": [
        -1.0,
        0
    ],
    "u7": [
        0.0,
        0
    ],
    "u8": [
        1.0,
        0
    ]
}

pos_copy = pos
## Not allowed, Python will only point this to the same object. 

old = ["u2", "u3", "u4"]
new = ["u4", "u3", "u2"]
def adjust_pos_data(old_order: list[str], new_order: list[str], orig_pos: dict[str, list[float]]) -> dict[str, list[float]]:
    """Danger of manipulation of the dictionary, uses deepcopy due to Py not being pass by value or pass by ref.  

    Args:
        old_order (list[str]): _description_
        new_order (list[str]): _description_
        orig_pos (dict[str, list[float]]): _description_

    Returns:
        dict[str, list[float]]: _description_
    """
    set_coords = []
    dict_copy = copy.deepcopy(orig_pos)
    for node in old_order:
        # print(node, pos[node])
        set_coords.append(dict_copy[node])
        
    for node in new_order:
    # assign it to its corresponding set coords in the pos_copy
        dict_copy[node] = set_coords[new_order.index(node)]
    
    return dict_copy

pos = adjust_pos_data(old, new, pos)

plt.figure(figsize=(5, 3))
nx.draw(
    G,
    pos=pos,
    with_labels=True,
    node_size=2000,
    node_color="lightgreen",
    font_size=10,
    font_weight="bold",
    arrows=True,
)

# Display the graph
plt.title("Graph with Multiple Layers and No Edges in Same Layer [original]")
plt.show()