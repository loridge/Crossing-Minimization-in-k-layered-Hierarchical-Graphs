import sys, os
import json
from networkx.readwrite import json_graph
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
import pprint
import csv
import networkx as nx, json
import re
from collections import defaultdict
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# debugging module imports
from k_layer_crossing import total_crossing_count_k_layer

# --- File in the same directory ---
file = "exp-9_8-8.json"

# Parse layer widths from filename
match = re.search(r'_(\d+(?:-\d+)*)\.json', file)
if match:
   layer_widths = [8] * 10
else:
    raise ValueError("Filename is malformed: " + file)

# Load the list of graphs
with open(file) as f:
    graph_list = json.load(f)

rows = []

for idx, graph in enumerate(graph_list):
    nodes = graph["nodes"]
    links = graph["links"]
    num_edges = len(links)
    total_nodes = len(graph["nodes"])
    num_layers = len(layer_widths)

    # Build edges
    # Handle edge format like {'nodes': ['u13', 'u24']}
    # print(links)
    edges = [{"nodes": [f"u{link['source']}", f"u{link['target']}"]} for link in links]
    
    print(edges)
    # Build layers for crossing count
    layer_map = defaultdict(set)
    for node in nodes:
        layer_map[node["layer"]].add(node["id"])
    layers = [layer_map[i] for i in sorted(layer_map)]

    # Crossing count
    # print(layers, edges)
    crossings = total_crossing_count_k_layer(layers, edges)

    # Edge density
    max_possible_edges = sum(
        layer_widths[i] * layer_widths[i + 1]
        for i in range(num_layers - 1)
    )
    edge_density = num_edges / max_possible_edges if max_possible_edges > 0 else 0

    rows.append({
        # "File": file,
        "Graph Index": idx,
        "Nodes": total_nodes,
        "Edges": num_edges,
        "Crossings": crossings,
        "Layers": num_layers,
        # "Nodes Per Layer": str(layer_widths),
        "Edge Density": round(edge_density, 4),
    })

# Output to CSV
df = pd.DataFrame(rows)
df.to_csv("appx_table_8-8.csv", index=False)
print(df)