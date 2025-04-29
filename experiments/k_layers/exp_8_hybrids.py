import random
import itertools
import networkx as nx
import sys, os
import time
import copy
from typing import (Dict, List,)
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
# for i in sys.path:
#     print(i)

from sifting import (
    sifting,
)

from bary_med.two_layer_barycenter import (
    barycenter,
    parse_edges,
    permutation,
    permutation_patarasuk,
)

from k_layered import (
    generate_k_layered_sparse_graph,
    visualize_k_layered_graph,
)

from k_layer_crossing import (
    total_crossing_count_k_layer,
)

snapshots = []

class Exp8Utility:
    @staticmethod
    def parse_layers_edges(layers, edges):
        """Preprocessing step for the data. Utility public method.
        Args:
            layers (_type_): _description_
            edges (_type_): _description_

        Returns:
            dict: _description_
        """
        k = len(layers)
        listify_layers = [list(i) for i in layers]
        map_idx_to_layer= {index: sublist for index, sublist in enumerate(listify_layers)}
        map_node_to_layer = {node: index_i for index_i, sublist in map_idx_to_layer.items() for _, node in enumerate(sublist)}
        
        # the dict indices will be layers 1 to n-1
        layerfy_edges={i:[] for i in range(1, k)}  # O(1) access 3:[nodes list], para hindi na lagi mag O(n) search for an edge
        
        for edge_obj in edges:
            u, v = edge_obj['nodes'] # uX, uY
            # i want to check it in the listify layer
            u_id = int(u[1:])  # Remove 'u' and convert to integer
            v_id = int(v[1:])
            # u and v cannot be in the same layer. hence we may check only the larger of the two nodes; corresponds to our definition of layerfy
            greater_id = u_id if u_id > v_id else v_id # guaranted that the nodes are from 1 to n-1 where n is len of layer list
            
            layerfy_edges[map_node_to_layer[greater_id]].append(edge_obj)
    
        return {
            'listify_layers':  listify_layers, 
            'layerfy_edges': layerfy_edges
        }

class BaseCutoffHybrid:
    """_summary_
    
        Args:
            layers (_type_): layers
            edges (_type_): edges object
            l_cutoff (__int__): cutoff value
            parsed_layer_edge_data: output of Exp8Utility.parse_layers_edges()
            comment_out: 0 for no, 1 for yes; comment outs the best_layer_struct deepcopy in the previous implementation
        Returns:
            dict: _description_
    """
    def __init__(
        self, 
        layers: List, 
        edges: List[List] , 
        l_cutoff: int, 
        parsed_layer_edge_data: Dict,
        comment_out = 1,
    ):
        
        if (0 <= l_cutoff <= (len(layers) - 1)) is False:
            raise ValueError(f"Invalid l_cutoff value, it must be from 0 to {len(layers) - 1}")
        
        self.layers = layers
        self.edges = edges 
        self.l_cutoff = l_cutoff
        self.forgiveness_number = 20
        self.k = len(layers)
        
        self.listify_layers = parsed_layer_edge_data['listify_layers']
        self.layerfy_edges = parsed_layer_edge_data['layerfy_edges']
    
        self.snapshots = [] # for the animation, note: comment out the snapshots.append below if going to proceed with experimentation.
        
        self.comment_out = comment_out # ito kasi ata dapat na correct behavior? na dapat hindi nagssave every after sweep 
        
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        """Reusable reorder function for code cleanliness.

        Args:
            free_layer (_type_): Also the 'bottom nodes.'
            fixed_layer (_type_): Also the 'upper nodes.'
            edges (_type_): _description_
            phase (_str_): Whether the algorithm is in the pre-cutoff or post-cutoff phase.
            direction (_type_): upward or downward
        """
        pass
    
    def execute(self) -> List[List]:
        """For the user, just comment out the snapshot append when you are going to proceed with the experiment.

        Returns:
            List[List]: _description_
        """
        min_crossings = total_crossing_count_k_layer(self.layers, self.edges)
        current_crossings = float('inf')
        best_layer_struct = copy.deepcopy(self.listify_layers)
        current_crossings = float('inf')
        current_layer_struct = [] # copy of the original 
        
        snapshots.append((copy.deepcopy(current_layer_struct), 0))
        if self.comment_out == 1: current_layer_struct = copy.deepcopy(best_layer_struct)
        if self.l_cutoff != 0:
            while self.forgiveness_number != 0:
                #### Downward Sweep
                if self.comment_out == 0: current_layer_struct = copy.deepcopy(best_layer_struct) # nag ooscillate yata sa animation due to this, since the current layer struct may not be the best_layer struct
                
                # print(f"Pre-cutoff free range down: {1, self.l_cutoff}")
                for i in range(1, self.l_cutoff + 1): # [1, l_cutoff] is the real range
                    # i are the indices of the free_layers in the downward sweep
                    self.snapshots.append((copy.deepcopy(current_layer_struct), -22)) 
                    reordered_layer = self.reorder_layer(current_layer_struct[i], current_layer_struct[i - 1], self.layerfy_edges[i], phase='pre-cutoff', direction='downward')
                    current_layer_struct[i] = reordered_layer
                    self.snapshots.append((copy.deepcopy(current_layer_struct), i))  # if permuted layer index is i

                ### Downward sweep checker
                current_crossings = total_crossing_count_k_layer(current_layer_struct, self.edges)
            
                if current_crossings < min_crossings:
                    min_crossings = current_crossings
                    best_layer_struct = copy.deepcopy(current_layer_struct)
                else: 
                    self.forgiveness_number -= 1
                    
                if self.forgiveness_number == 0: break
                
                #### Upward Sweep
                # current_layer_struct = copy.deepcopy(best_layer_struct) # nag ooscillate yata sa animation due to this, since the current layer struct may not be the best_layer struct
                if self.comment_out == 0: current_layer_struct = copy.deepcopy(best_layer_struct)
                # print(f"Pre-cutoff free range up: {self.l_cutoff - 1, 0}")
                for j in range(self.l_cutoff - 1, -1, -1): # [l_cutoff - 1, 0] is the real range
                    # j should be the indices of the 'top_layer' that is the free_layer in upward sweep
                    self.snapshots.append((copy.deepcopy(current_layer_struct), -22)) 
                    reordered_layer = self.reorder_layer(current_layer_struct[j], current_layer_struct[j + 1], self.layerfy_edges[j + 1], phase='pre-cutoff', direction='upward')
                    current_layer_struct[j] = reordered_layer
                    self.snapshots.append((copy.deepcopy(current_layer_struct), j))  # if permuted layer index is j

                ### Upward sweep checker
                current_crossings = total_crossing_count_k_layer(current_layer_struct, self.edges)
            
                if current_crossings < min_crossings:
                    min_crossings = current_crossings   ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
                    best_layer_struct = copy.deepcopy(current_layer_struct)
                else: # current >= min # did not improve or worse.
                    self.forgiveness_number -= 1
                    
                if self.forgiveness_number == 0: break
                
        self.forgiveness_number = 20   # replenish the forgiveness number
        
        if self.l_cutoff != (self.k - 1):
            while self.forgiveness_number != 0:
                #### Downward Sweep
                # current_layer_struct = copy.deepcopy(best_layer_struct) # nag ooscillate yata sa animation due to this, since the current layer struct may not be the best_layer struct
                if self.comment_out == 0: current_layer_struct = copy.deepcopy(best_layer_struct)
                # print(f"Post-cutoff free range down: {self.l_cutoff + 1, self.k - 1}")
                for i in range(self.l_cutoff + 1, self.k): # [l_cutoff + 1, k - 1] is the real range
                    # i are the indices of the free_layers in the downward sweep
                    self.snapshots.append((copy.deepcopy(current_layer_struct), -22)) 
                    reordered_layer = self.reorder_layer(current_layer_struct[i], current_layer_struct[i - 1], self.layerfy_edges[i], phase='post-cutoff', direction='downward')
                    current_layer_struct[i] = reordered_layer
                    self.snapshots.append((copy.deepcopy(current_layer_struct), i))  # if permuted layer index is i

            
                ### Downward sweep checker
                current_crossings = total_crossing_count_k_layer(current_layer_struct, self.edges)
            
                if current_crossings < min_crossings:
                    min_crossings = current_crossings ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
                    best_layer_struct = copy.deepcopy(current_layer_struct)
                else: # current >= min # did not improve or worse.
                    self.forgiveness_number -= 1
                    
                if self.forgiveness_number == 0: break
                
                #### Upward Sweep
                # print(f"Post-cutoff free range up: {self.k - 2, self.l_cutoff}")
                # current_layer_struct = copy.deepcopy(best_layer_struct) # oscillation source
                if self.comment_out == 0: current_layer_struct = copy.deepcopy(best_layer_struct)
                for j in range(self.k - 2, self.l_cutoff - 1, -1): # [k - 2, l_cutoff] is the real range ng free # manipulated yung l_cutoff
                # for j in range(self.k - 2, self.l_cutoff+1, -1): # [k - 2, l_cutoff + 2] is the real range # unmanipulated yung l_cutoff
                    # j should be the indices of the 'top_layer' that is the free_layer in upward sweep
                    self.snapshots.append((copy.deepcopy(current_layer_struct), -22)) 
                    reordered_layer = self.reorder_layer(current_layer_struct[j], current_layer_struct[j + 1], self.layerfy_edges[j + 1], phase='post-cutoff', direction='upward')
                    # print(f"free {j}, fixed {j+1}")
                    current_layer_struct[j] = reordered_layer
                    self.snapshots.append((copy.deepcopy(current_layer_struct), j))  # if permuted layer index is j

                ### Upward sweep checker
                current_crossings = total_crossing_count_k_layer(current_layer_struct, self.edges)
            
                if current_crossings < min_crossings:
                    min_crossings = current_crossings   ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
                    best_layer_struct = copy.deepcopy(current_layer_struct)
                else: # current >= min # did not improve or worse.
                    self.forgiveness_number -= 1
                    
                if self.forgiveness_number == 0: break
            
        return best_layer_struct
    
    def animate_snapshots(self, delay=0.5):
        """
        Animates snapshots of layer states with highlighted permuted layer.

        Args:
            snapshots (List[Tuple[List[List[str]], int]]): Each element is (layers, permuted_layer_index)
            edges (List[Dict]): List of edge dictionaries.
            delay (float): Pause between frames in seconds.
        """
        for idx, (layer_snapshot, permuted_idx) in enumerate(self.snapshots):
            plt.clf()
            G = nx.Graph()
            pos = {}
            node_colors = {}

            formatted_layers = [[f"u{n}" if not isinstance(n, str) else n for n in layer] for layer in layer_snapshot]

            for y, layer in enumerate(formatted_layers):
                for x, node in enumerate(layer):
                    G.add_node(node)
                    pos[node] = (x, -y)
                    node_colors[node] = "red" if y == permuted_idx else "lightblue"

            for edge in self.edges:
                u, v = edge['nodes']
                if u in G and v in G:
                    G.add_edge(u, v)

            nx.draw(
                G, pos,
                with_labels=True,
                node_size=500,
                node_color=[node_colors[n] for n in G.nodes()],
                edge_color="gray",
                font_weight="bold",
                font_size=8
            )
            plt.title(f"Step {idx + 1} (Layer {permuted_idx} permuted)")
            plt.pause(delay)

        plt.show()
    
    def animate_snapshots_to_video(self, output_filename="animation.mp4", fps=1):
        """
        Exports animated graph snapshots to a video file.
        
        Args:
            snapshots (List[Tuple[List[List[str]], int]]): Snapshots of layer states and permuted index.
            edges (List[Dict]): Edge list with 'nodes' keys.
            output_filename (str): Output video filename (.mp4).
            fps (int): Frames per second (lower = slower animation).
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        G = nx.Graph()

        def update(frame_idx):
            ax.clear()
            layer_snapshot, permuted_idx = self.snapshots[frame_idx]
            G.clear()
            pos = {}
            node_colors = {}

            formatted_layers = [[f"u{n}" if not isinstance(n, str) else n for n in layer] for layer in layer_snapshot]

            for y, layer in enumerate(formatted_layers):
                for x, node in enumerate(layer):
                    G.add_node(node)
                    pos[node] = (x, -y)
                    node_colors[node] = "red" if y == permuted_idx else "lightblue"

            for edge in self.edges:
                u, v = edge["nodes"]
                if u in G and v in G:
                    G.add_edge(u, v)

            nx.draw(
                G, pos,
                ax=ax,
                with_labels=True,
                node_size=500,
                node_color=[node_colors[n] for n in G.nodes()],
                edge_color="gray",
                font_weight="bold",
                font_size=8,
            )
            ax.set_title(f"Step {frame_idx + 1} (Layer {permuted_idx} permuted)")
            ax.set_axis_off()

        ani = FuncAnimation(fig, update, frames=len(self.snapshots), repeat=False)

        # Save to MP4 (requires ffmpeg)
        writer = FFMpegWriter(fps=fps, bitrate=800)  # Lower bitrate = smaller file
        ani.save(output_filename, writer=writer)
        print(f"Animation saved to {output_filename}")
    
class BarySiftingCutoffHybrid(BaseCutoffHybrid):
    def __init__(
        self, 
        layers: List, 
        edges: List[List] , 
        l_cutoff: int, 
        parsed_layer_edge_data: Dict,
        comment_out = 1
    ):
        super().__init__(layers, edges, l_cutoff, parsed_layer_edge_data, comment_out) 
      
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        if phase == 'pre-cutoff':
            formatted_edges = parse_edges(edges, fixed_layer, free_layer)
            return barycenter(free_layer, fixed_layer, formatted_edges)
        elif phase == 'post-cutoff':
            return sifting(free_layer, fixed_layer, edges, direction)
        else:
            raise ValueError("Invalid phase argument.")
        
class PermuSiftingCutoffHybrid(BaseCutoffHybrid):
    def __init__(
        self, 
        layers: List, 
        edges: List[List] , 
        l_cutoff: int, 
        parsed_layer_edge_data: Dict,
        comment_out = 1
    ):
        super().__init__(layers, edges, l_cutoff, parsed_layer_edge_data, comment_out)
      
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        if phase == 'pre-cutoff':
            reordered_layer, _ = permutation(fixed_layer, free_layer, edges)
            return reordered_layer
        elif phase == 'post-cutoff':
            return sifting(free_layer, fixed_layer, edges, direction)
        else:
            raise ValueError("Invalid phase argument.")
    
class PermuBaryCutoffHybrid(BaseCutoffHybrid):
    def __init__(
        self, 
        layers: List, 
        edges: List[List] , 
        l_cutoff: int, 
        parsed_layer_edge_data: Dict,
        comment_out = 1
    ):
        super().__init__(layers, edges, l_cutoff, parsed_layer_edge_data, comment_out)
      
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        if phase == 'pre-cutoff':
            reordered_layer, _ = permutation(fixed_layer, free_layer, edges)
            return reordered_layer
        elif phase == 'post-cutoff':
            formatted_edges = parse_edges(edges, fixed_layer, free_layer)
            return barycenter(free_layer, fixed_layer, formatted_edges)
        else:
            raise ValueError("Invalid phase argument.")
    
class SiftingBaryCutoffHybrid(BaseCutoffHybrid):
    def __init__(
        self, 
        layers: List, 
        edges: List[List] , 
        l_cutoff: int, 
        parsed_layer_edge_data: Dict,
        comment_out = 1,
    ):
        super().__init__(layers, edges, l_cutoff, parsed_layer_edge_data, comment_out)
      
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        if phase == 'pre-cutoff':
            return sifting(free_layer, fixed_layer, edges, direction)
        elif phase == 'post-cutoff':
            formatted_edges = parse_edges(edges, fixed_layer, free_layer)
            return barycenter(free_layer, fixed_layer, formatted_edges)
        else:
            raise ValueError("Invalid phase argument.")

if __name__ == "__main__":
    k = 10
    n = 7
    m = 7
    nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, m)
    
    x = total_crossing_count_k_layer(layers, edges)
    print("Original graph " + str(x))
    
    parsed_data = Exp8Utility.parse_layers_edges(layers, edges)
    
    #uncommented barysift
    bary_sift = BarySiftingCutoffHybrid(layers, edges, l_cutoff=2, parsed_layer_edge_data=parsed_data, comment_out=0)
    barysift_reordered = bary_sift.execute()
    barysift_reordered_count = total_crossing_count_k_layer(barysift_reordered, edges)
    print(f"BarycenterSifting {barysift_reordered_count}")
    
    #commented barysift
    bary_sifter = BarySiftingCutoffHybrid(layers, edges, l_cutoff=2, parsed_layer_edge_data=parsed_data, comment_out=1)
    barysift_reordereder = bary_sifter.execute()
    barysift_reordered_counter = total_crossing_count_k_layer(barysift_reordereder, edges)
    print(f"BarycenterSifting {barysift_reordered_counter}")

    permusifting = PermuSiftingCutoffHybrid(layers, edges, l_cutoff=2, parsed_layer_edge_data=parsed_data, comment_out=1)
    permusifting_reorderer = permusifting.execute()
    permusifting_reordered_counter = total_crossing_count_k_layer(permusifting_reorderer, edges)
    print(f"Permusifting {permusifting_reordered_counter}")
    
    ########## ANIMATION 
    ### may bug, the cut-off layer just oscillates kapag post-cutoff phase na
    ### new update, added the comment_out for this
    # bary_sift.animate_snapshots() # for observing the behavior