import networkx as nx
import matplotlib.pyplot as plt
import json

# Graph generation
filepath = './10nodes/grafo155.10.json'
graph_file = open(filepath, 'r')

data = json.load(graph_file)
print(type(data), 'debug') #debug

nodes = data["nodes"]

edges = data["edges"]

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
print('POS dict object!')
## Crossing function
# objective function in literature <stallman>
def cross_count(fixed_layer: list[str], free_layer: list[str], pos_data):
    """
    Calculate the number of edge crossings between two layers in a bipartite graph.

    This function uses the crossing objective function as described in the 
    implementation by https://studenttheses.uu.nl/bitstream/handle/20.500.12932/46720/final_Bachelor_Thesis_Mathematics.pdf?sequence=1&isAllowed=y
    to count all of the crossings present in a bipartite graph. The function
    takes two lists of node labels representing two layers of the graph and
    the positional data of the nodes in the Cartesian plane.

    Args:
        U is free, L is fixed
        layer1_nodes (list of str): List of node labels in the first layer.
        layer2_nodes (list of str): List of node labels in the second layer.
        pos_data (dict): Dictionary containing the positional data of the nodes.
                         The keys are node labels, and the values are (x, y) tuples
                         representing the positions of the nodes.

    Returns:
        int: The total number of edge crossings between the two layers.
    """
    crossing_total = 0
    
    for u_node in free_layer:
        neighbor_u_node = []
        # fill the neighbor u node; neighbors of u_node
        # TODO: implement filling of neighbor_u_node
        
        for v_node in neighbor_u_node:
            u_prime_nodes = []
            # TODO: implement filling u_prime, list of node u that are positioned to the left of u
            for u_prime in u_prime_nodes:
                # TODO: implement filtering of nodes 
                result = []
                
                crossing_total += len(result)
        pass
    
    
    pass

# Sifting function

def sifting():
    pass

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