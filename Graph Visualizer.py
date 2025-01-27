## GRAPH VISUALIZER 
## Makes sure that there are no same layer edges

import networkx as nx
import matplotlib.pyplot as plt

# Define the graph structure with multiple layers
nodes = [
    {"id": "u1", "layer": 1},
    {"id": "u2", "layer": 2},
    {"id": "u3", "layer": 2},
    {"id": "u4", "layer": 2},
    {"id": "u5", "layer": 1},
    {"id": "u6", "layer": 0},
    {"id": "u7", "layer": 0},
    {"id": "u8", "layer": 0}
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
    G.add_node(node["id"], depth=node["layer"])  # Use 'layer' as 'depth'

# Add edges to the graph, ensuring no same-layer edges
for edge in edges:
    node1, node2 = edge["nodes"]
    if G.nodes[node1]["depth"] != G.nodes[node2]["depth"]:  # Check depths
        G.add_edge(node1, node2)

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

# Draw the graph
plt.figure(figsize=(8, 6))
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
plt.title("Graph with Multiple Layers and No Edges in Same Layer")
plt.show()
