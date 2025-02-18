import networkx as nx
import matplotlib.pyplot as plt
import json

import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crossing_function.crossing_func import cross_count



# Graph generation
filepath = './10nodes/grafo155.10.json'
graph_file = open(filepath, 'r')
data = json.load(graph_file)

nodes = data["nodes"]

edges = data["edges"]


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

print(layered_pos, 'LAYERED POS')
# Initial placement (place the nodes in horizontal layers)
pos = {}
layer_height = 2  # Vertical spacing between layers
for layer, nodes_in_layer in layered_pos.items():
    # Sort nodes in each layer by their 'id' in increasing order
    nodes_in_layer.sort()  # Sort alphabetically by id
    x_offset = -(len(nodes_in_layer) - 1) / 2  # Center nodes horizontally
    for i, node in enumerate(nodes_in_layer):
        pos[node] = (x_offset + i, -layer * layer_height)

print(json.dumps(pos, indent = 4))
print('POS dict object, DEBUGGING')

## TODO:  a check whether 2 provided layers are +1 of each other, for the layer by layer function

## NOTE: 0 is the highest layer numbering; and the greater its absolute value, the lower it is placed in the graph
free_layer_no = 4
fixed_layer_no = 3
free_layer = layered_pos[free_layer_no]
fixed_layer = layered_pos[fixed_layer_no]

print(free_layer, 'free_layer')
print(fixed_layer, 'fixed_layer')
print('Total Layer Crossing Count: ', cross_count(fixed_layer, free_layer, pos, edges, layered_pos))    

# Draw the graph
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
plt.title("Graph with Multiple Layers and No Edges in Same Layer")
plt.show()

graph_file.close()