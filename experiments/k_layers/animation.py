import matplotlib.pyplot as plt
import networkx as nx
import time

def show_layered_stopmotion(layers_list, edges, pause=1.0):
    """
    layers_list: List of layered node arrangements (like from each iteration)
    edges: list of dicts like {'nodes': ['u1', 'u2']}
    pause: time between frames
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for step_idx, layers in enumerate(layers_list):
        ax.clear()
        G = nx.Graph()
        
        # Add nodes and positions layer by layer
        pos = {}
        for layer_idx, layer in enumerate(layers):
            for i, node in enumerate(layer):
                G.add_node(node)
                pos[node] = (i, -layer_idx)

        # Add edges
        for edge in edges:
            u, v = edge["nodes"]
            G.add_edge(u, v)

        nx.draw(G, pos, with_labels=True, node_color='skyblue', ax=ax)
        ax.set_title(f"Step {step_idx}")
        plt.pause(pause)

    plt.show()
    
layers_0 = [['u1', 'u2'], ['u3', 'u4']]
layers_1 = [['u2', 'u1'], ['u4', 'u3']]
layers_2 = [['u1', 'u2'], ['u3', 'u4']]

edges = [{'nodes': ['u1', 'u3']}, {'nodes': ['u2', 'u4']}]

show_layered_stopmotion([layers_0, layers_1, layers_2], edges, pause=1.5)