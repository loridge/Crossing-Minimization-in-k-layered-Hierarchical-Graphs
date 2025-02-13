import networkx as nx
import matplotlib.pyplot as plt
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crossing_function.crossing_func import cross_count
from crossing_function.crossing_utils import node_neighbors
import bisect 
import itertools
from sifting_utils import do_sifting

# Graph generation
filepath = './10nodes/grafo155.10.json'
graph_file = open(filepath, 'r')

data = json.load(graph_file)
print(type(data), 'debug') #debug

nodes = data["nodes"]

edges = data["edges"]

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

# Sifting function
def sifting(free_layer: list[str], fixed_layer: list[str], edges: list, pos):
    """
        Must output a reordered freelayer positional xy values
        Sifting concerns about ordering decisions.
        
        
        
        output must be new graph positioning. 
    Args:
        free_layer (list[str]): _description_
        fixed_layer (list[str]): _description_
        pos: contains the x-coordinates
    """    
    
    # Make a PRIORITY QUEUE for nodes in descending order of their indegrees.
    ## element format (node, indegree)    
    indeg_prio_queue = []
    
    for node in free_layer:
        indeg_cnt = len(node_neighbors(node, edges, fixed_layer))
        indeg_prio_queue.append((node, indeg_cnt))
        
    sorted_indeg_prio_queue = [item for item, _ in sorted(indeg_prio_queue, key=lambda x: x[1], reverse=True)] # ditching the indegree values after the sorting has been done
    # print(sorted(indeg_prio_queue, key=lambda x: x[1], reverse=True))
    # print("sorted_indeg_prio_queue", sorted_indeg_prio_queue)
    
    # initialize current free layer order, based on how it was initialized earlier
    # TODO: use the pos to rearrange free_layer, since free_layer only contains the nodes needed, not the order
    current_layer_order = [] 

    for node in free_layer:
        x_coord = pos[node][0]
        node_info = (node, x_coord)
        bisect.insort(current_layer_order, node_info)   
    
    # now we assume that the order of current_layer_order is based on the order as stated in pos and not in the ordering seen in free_layer list

    print("CORRECT CURRENT LAYER, not extracted - sifting")
    print(current_layer_order)    
    current_layer_order=[node for node, _ in current_layer_order]
    
    for node in sorted_indeg_prio_queue:
        new_layer_order = do_sifting(node, current_layer_order, fixed_layer, pos, edges)
        current_layer_order = new_layer_order
    
    
    
    
    
    # X-COORD PROBLEM
    # pag sinift mo ba, pano mag-aadjust x-coords?? how will it be recomputed?
    # the crossing function only uses the positions, but let us check how this will work if only the node are given
    # barycenter explicity uses it, but for sifting??
    ## does it preserve the original x-coords na parang slot machine iinsert mo doon, or magbabago x-coords
    
    # sifting with new insertion, x-coords must be readjusted
    # layer ordering is based on x-coords
    ## how does sifting consider x-coordinates?
    
    # READJUST NEW GRAPH COORDINATES
    
    
    # return new graph coords, current returnng layer order is temporary
    return current_layer_order

    # will the output of this sifting function be array((node, x-coords)), then the pos dict will be edited at the layer-by-layer code or
    # the graph as a whole???, but hey we are only localized in this view.
    
# note, the higher the layer number, the lower it is on the graph
free_layer_no = 2
fixed_layer_no = 1
free_layer = layered_pos[free_layer_no]
fixed_layer = layered_pos[fixed_layer_no]

sifting(free_layer, fixed_layer, edges, pos)


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