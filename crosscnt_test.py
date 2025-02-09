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

target = "u1"

neighbors = []

for edge_data in edges:
    edge_node_arr = edge_data["nodes"]
    if target in edge_node_arr:
        other_node = edge_node_arr[1] if edge_node_arr[0] == target else edge_node_arr[0]
        neighbors.append(other_node)



print(neighbors)