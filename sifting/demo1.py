from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sifting_2 import sifting
from sifting_util2 import update_positions

# Graph generation
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
new_edges = []
for edge in edges:
    node1, node2 = edge["nodes"]
    if G.nodes[node1]["depth"] != G.nodes[node2]["depth"]:  # Check depths
        G.add_edge(node1, node2)
        new_edges.append(edge)
edges = new_edges

# Initialize positions for nodes grouped by depths
layered_pos = {}
for node in G.nodes():
    depth = G.nodes[node]["depth"]
    if depth not in layered_pos:
        layered_pos[depth] = []
    layered_pos[depth].append(node)

# Initial placement (place the nodes in horizontal layers)
pos = {}
layer_height = 2  # Vertical spacing between layers
for layer, nodes_in_layer in layered_pos.items():
    # Sort nodes in each layer by their 'id' in increasing order
    nodes_in_layer.sort()  # Sort alphabetically by id
    x_offset = -(len(nodes_in_layer) - 1) / 2  # Center nodes horizontally
    for i, node in enumerate(nodes_in_layer):
        pos[node] = (x_offset + i, -layer * layer_height)

print("Initial positions:")
print(json.dumps(pos, indent=1))

# Note, the higher the layer number, the lower it is on the graph
free_layer_no = 2
fixed_layer_no = 1
free_layer = layered_pos[free_layer_no]
fixed_layer = layered_pos[fixed_layer_no]

sift_res = sifting(free_layer, fixed_layer, edges, verbose=1)
minimized_layer = sift_res

# Adjust positions based on the minimized layer order
updated_pos = update_positions(free_layer, minimized_layer, pos)

print("Original layer:")
print(free_layer)
print("Minimized layer:")
print(minimized_layer)
print("Updated positions:")
print(json.dumps(updated_pos, indent=1))

# Draw the graph before updating positions
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
nx.draw(
    G,
    pos=pos,
    with_labels=True,
    node_size=2000,
    node_color="lightblue",
    font_size=10,
    font_weight="bold",
    arrows=True,
)
plt.title("Graph Before Sifting")

# Draw the graph after updating positions
plt.subplot(1, 2, 2)
nx.draw(
    G,
    pos=updated_pos,
    with_labels=True,
    node_size=2000,
    node_color="lightgreen",
    font_size=10,
    font_weight="bold",
    arrows=True,
)
plt.title("Graph After Sifting")

# Display the graphs
plt.show()