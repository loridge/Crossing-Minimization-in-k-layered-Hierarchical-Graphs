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
        
## Crossing function
# objective functiion in literature
def cross_count():
    pass

# Sifting function

def sifting():
    pass
print(pos)