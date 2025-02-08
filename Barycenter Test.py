import networkx as nx
import matplotlib.pyplot as plt

# Define the graph structure for a three-layer graph
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
    G.add_node(node['id'], layer=node['layer'])

# Add edges to the graph
for edge in edges:
    G.add_edge(edge['nodes'][0], edge['nodes'][1])

# Initialize positions for three layers
layered_pos = {0: [], 1: [], 2: []}
for node in G.nodes():
    layer = G.nodes[node]['layer']
    layered_pos[layer].append(node)

# Initial placement (place the nodes in horizontal layers)
pos = {}
layer_height = 2
for layer, nodes_in_layer in layered_pos.items():
    print(nodes_in_layer)
    print('\n')
    x_offset = -(len(nodes_in_layer) - 1) / 2  # Center nodes horizontally
    for i, node in enumerate(nodes_in_layer):
        pos[node] = (x_offset + i, -layer * layer_height)

print(pos)
plt.figure(figsize=(10, 8))
nx.draw(
    G, 
    pos=pos, 
    with_labels=True, 
    node_size=2000, 
    node_color="lightblue", 
    font_size=10, 
    font_weight="bold", 
    arrows=True
)

# Display the graph
plt.title("Three-Layer Graph with Barycenter Ordering Within Layers")
plt.show()

# Function to calculate barycenters for nodes within a layer based on neighbors in the previous layer
def calculate_barycenters(current_layer_nodes, prev_layer_nodes, pos, G):
    barycenters = {}
    for node in current_layer_nodes:
        neighbors = [neighbor for neighbor in G.neighbors(node) if neighbor in prev_layer_nodes]
        if neighbors:
            barycenter = sum(pos[neighbor][0] for neighbor in neighbors) / len(neighbors)
        else:
            barycenter = 0
        barycenters[node] = barycenter
    return barycenters

# Step 1: Sort Layer 2 based on Layer 1
barycenters_layer_2 = calculate_barycenters(layered_pos[2], layered_pos[1], pos, G)
sorted_layer_2 = sorted(layered_pos[2], key=lambda node: barycenters_layer_2[node])
x_offset = -(len(sorted_layer_2) - 1) / 2
for i, node in enumerate(sorted_layer_2):
    pos[node] = (x_offset + i, pos[node][1])  # Adjust only horizontal position

# Step 2: Sort Layer 1 based on Layer 0
barycenters_layer_1 = calculate_barycenters(layered_pos[1], layered_pos[0], pos, G)
sorted_layer_1 = sorted(layered_pos[1], key=lambda node: barycenters_layer_1[node])
x_offset = -(len(sorted_layer_1) - 1) / 2
for i, node in enumerate(sorted_layer_1):
    pos[node] = (x_offset + i, pos[node][1])  # Adjust only horizontal position

# Draw the graph
plt.figure(figsize=(10, 8))
nx.draw(
    G, 
    pos=pos, 
    with_labels=True, 
    node_size=2000, 
    node_color="lightblue", 
    font_size=10, 
    font_weight="bold", 
    arrows=True
)

# Display the graph
plt.title("Three-Layer Graph with Barycenter Ordering Within Layers")
plt.show()
