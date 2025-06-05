# testing
import networkx as nx
import json, sys, os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',  ))


if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
from k_layer_crossing import total_crossing_count_k_layer
from k_layered import generate_k_layered_sparse_graph

# Step 1: Generate a graph
# G = nx.erdos_renyi_graph(n=5, p=0.6)  # random graph with 5 nodes
nodes, edges, G, layers = generate_k_layered_sparse_graph(10, 6, 6)
# Step 2: Convert graph to node-link data (JSON-serializable)
print(edges)
print(nodes)
data = nx.readwrite.json_graph.node_link_data(G)

# Step 3: Append to an array of graphs
graph_array = []
graph_array.append(data)

# Step 4: (Optional) Output as JSON string
# json_output = json.dumps(graph_array, indent=2)
# Print the JSON string
# print(json_output)
with open("graph_jsong.json", "w") as f:
    json.dump(graph_array, f, indent=2)