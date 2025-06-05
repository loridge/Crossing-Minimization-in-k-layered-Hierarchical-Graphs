import random
import itertools
import networkx as nx
import sys, os
import time
import copy
from typing import (
    Dict, 
    List, 
    Tuple
)
import matplotlib.pyplot as plt
from matplotlib.animation import (
    FuncAnimation, 
    FFMpegWriter
)
from abc import (
    ABC, 
    abstractmethod
)

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
# for i in sys.path:
#     print(i)

from two_layer_functions import (
    sifting,
)

from two_layer_functions.two_layer_barycenter import (
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

class BaseCutoffHybrid(ABC):
    """Base class for the other algorithms
    
        Args:
            layers (_type_): layers
            edges (_type_): edges object
            l_cutoff (__int__): cutoff value
            parsed_layer_edge_data: output of static method parse_layers_edges()
            comment_out: 0 for no, 1 for yes; comment outs the best_layer_struct deepcopy in the previous implementation. Default is Yes (new imple)
            capture: 0 for no, 1 for yes; indicates whether every layer-by-layer manipulation is captured for animation purposes. Default is No.
        Returns:
            dict: _description_
    """
    def __init__(
        self, 
        layers: List, 
        edges: List[List] , 
        l_cutoff: int, 
        parsed_layer_edge_data: Dict,
        comment_out = 1, # ito kasi ata dapat na correct behavior? na dapat hindi nagssave every after sweep 
        capture = 0, # default is do not capture snapshots
    ):
        
        if (0 <= l_cutoff <= (len(layers) - 1)) is False:
            raise ValueError(f"Invalid l_cutoff value, it must be from 0 to {len(layers) - 1}")
        
        self.layers = layers
        self.edges = edges 
        self.l_cutoff = l_cutoff
        self.listify_layers = parsed_layer_edge_data['listify_layers']
        self.layerfy_edges = parsed_layer_edge_data['layerfy_edges']
        self.comment_out = comment_out 
        self.capture = capture
        
        self.forgiveness_number = 20
        self.k = len(layers)
        
        self.snapshots = [] # for the animation, note: turn off the snapshots.append below if going to proceed with experimentation.
        
    @abstractmethod
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        """ Reorder the free layer based on the fixed layer and edge structure.
        This method must be overridden in any subclass.
        
        Args:
            free_layer (List): The layer to be reordered. Also the 'bottom nodes.'
            fixed_layer (List): The fixed layer used as a reference. Also the 'upper nodes.'
            edges (List[Dict]): List of edge dictionaries between layers.
            phase (str): Either 'pre-cutoff' or 'post-cutoff'.
            direction (str): Direction of traversal. Either 'upward' or 'downward'.
        """
        pass
    
    @staticmethod # kasi dapat icacall lang sya once para di masyado expensive, kaya static method
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
    
    def execute(self) -> Tuple[List[List], Tuple]:
        """Executes the layer-by-layer sweep algorithm.

        Returns:
            reordered_ds_and_time_elapsed (_tuple[list[list], tuple]_): Outputs the reordered layer data structure and the time elapsed for every LbL sweep algorithm.
        """
        # timer_elapsed_bin: List[Tuple] = [] # e.g. (5.74, 8.53) corresponding to (time elapsed for layer-by-layer sifting, TE for LbL barycenter)
        # mali pala ata to
        
        
        min_crossings = total_crossing_count_k_layer(self.layers, self.edges)
        current_crossings = float('inf')
        best_layer_struct = copy.deepcopy(self.listify_layers)
        current_crossings = float('inf')
        current_layer_struct = [] # copy of the original 
        
        if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), 0, -1))
        if self.comment_out == 1: current_layer_struct = copy.deepcopy(best_layer_struct)
        
        start_pre_cutoff = time.perf_counter() 
        if self.l_cutoff != 0:
            while self.forgiveness_number != 0:
                #### Downward Sweep
                if self.comment_out == 0: current_layer_struct = copy.deepcopy(best_layer_struct) # nag ooscillate yata sa animation due to this, since the current layer struct may not be the best_layer struct
                
                # print(f"Pre-cutoff free range down: {1, self.l_cutoff}")
                for i in range(1, self.l_cutoff + 1): # [1, l_cutoff] is the real range
                    # i are the indices of the free_layers in the downward sweep
                    if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), i, -1)) 
                    reordered_layer = self.reorder_layer(current_layer_struct[i], current_layer_struct[i - 1], self.layerfy_edges[i], phase='pre-cutoff', direction='downward')
                    current_layer_struct[i] = reordered_layer
                    if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), i, 1))  # if permuted layer index is i

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
                    if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), j, -1)) 
                    reordered_layer = self.reorder_layer(current_layer_struct[j], current_layer_struct[j + 1], self.layerfy_edges[j + 1], phase='pre-cutoff', direction='upward')
                    current_layer_struct[j] = reordered_layer
                    if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), j, 1))  # if permuted layer index is j

                ### Upward sweep checker
                current_crossings = total_crossing_count_k_layer(current_layer_struct, self.edges)
            
                if current_crossings < min_crossings:
                    min_crossings = current_crossings   ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
                    best_layer_struct = copy.deepcopy(current_layer_struct)
                else: # current >= min # did not improve or worse.
                    self.forgiveness_number -= 1
                    
                if self.forgiveness_number == 0: break
        end_pre_cutoff = time.perf_counter()
        pre_cutoff_elapsed = end_pre_cutoff - start_pre_cutoff
        
                
        self.forgiveness_number = 20   # replenish the forgiveness number
        
        start_post_cutoff = time.perf_counter()
        if self.l_cutoff != (self.k - 1):
            while self.forgiveness_number != 0:
                #### Downward Sweep
                # current_layer_struct = copy.deepcopy(best_layer_struct) # nag ooscillate yata sa animation due to this, since the current layer struct may not be the best_layer struct
                if self.comment_out == 0: current_layer_struct = copy.deepcopy(best_layer_struct)
                # print(f"Post-cutoff free range down: {self.l_cutoff + 1, self.k - 1}")
                for i in range(self.l_cutoff + 1, self.k): # [l_cutoff + 1, k - 1] is the real range
                    # i are the indices of the free_layers in the downward sweep
                    if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), i, -1)) 
                    reordered_layer = self.reorder_layer(current_layer_struct[i], current_layer_struct[i - 1], self.layerfy_edges[i], phase='post-cutoff', direction='downward')
                    current_layer_struct[i] = reordered_layer
                    if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), i, 1))  # if permuted layer index is i

            
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
                    if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), j, -1)) 
                    reordered_layer = self.reorder_layer(current_layer_struct[j], current_layer_struct[j + 1], self.layerfy_edges[j + 1], phase='post-cutoff', direction='upward')
                    # print(f"free {j}, fixed {j+1}")
                    current_layer_struct[j] = reordered_layer
                    if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), j, 1))  # if permuted layer index is j

                ### Upward sweep checker
                current_crossings = total_crossing_count_k_layer(current_layer_struct, self.edges)
            
                if current_crossings < min_crossings:
                    min_crossings = current_crossings   ### DO WE IMPLEMENT THE SAVING OF THE DATA STRUCTURE
                    best_layer_struct = copy.deepcopy(current_layer_struct)
                else: # current >= min # did not improve or worse.
                    self.forgiveness_number -= 1
                    
                if self.forgiveness_number == 0: break
        end_post_cutoff = time.perf_counter()
        post_cutoff_elapsed = end_post_cutoff - start_post_cutoff
        
        total_elapsed = end_post_cutoff - start_pre_cutoff
        
        return best_layer_struct, (total_elapsed, pre_cutoff_elapsed, post_cutoff_elapsed)
    
    def execute_onesweep(self) -> List[List]:
        """For testing, deprecated, to be updated soon

        Returns:
            List[List]: _description_
        """
        
        best_layer_struct = copy.deepcopy(self.listify_layers)
        current_layer_struct = [] # copy of the original 
        
        if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), 0))
        if self.comment_out == 1: current_layer_struct = copy.deepcopy(best_layer_struct)
        
        for i in range(1, self.k):
            if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), -22)) 
            reordered_layer = self.reorder_layer(current_layer_struct[i], current_layer_struct[i - 1], self.layerfy_edges[i], phase='pre-cutoff', direction='downward')
            current_layer_struct[i] = reordered_layer
            if self.capture: self.snapshots.append((copy.deepcopy(current_layer_struct), i))  # if permuted layer index is i
        
        best_layer_struct = copy.deepcopy(current_layer_struct)
        
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
                    node_colors[node] = "orange" if y == permuted_idx else "lightblue"

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
    
    def create_animation(self, filename="animation.mp4", delay=500):
        fig, ax = plt.subplots(figsize=(10, 6))
        # print(f"{self.snapshots}")
        def update(frame_idx):
            ax.clear()
            layer_snapshot, permuted_idx, indicator_if_being_manipulated = self.snapshots[frame_idx]
            G = nx.Graph()
            pos = {}
            node_colors = {}

            formatted_layers = [[f"u{n}" if not isinstance(n, str) else n for n in layer] for layer in layer_snapshot]
            
            for y, layer in enumerate(formatted_layers):
                for x, node in enumerate(layer):
                    G.add_node(node)
                    pos[node] = (x, -y)
                    node_colors[node] = "orange" if y == permuted_idx and indicator_if_being_manipulated == 1 else "lightblue"

            for edge in self.edges:
                u, v = edge['nodes']
                if u in G and v in G:
                    G.add_edge(u, v)

            nx.draw(
                G, pos, ax=ax,
                with_labels=True,
                node_size=500,
                node_color=[node_colors[n] for n in G.nodes()],
                edge_color="gray",
                font_weight="bold",
                font_size=8
            )
            
            if indicator_if_being_manipulated == 1:
                ax.set_title(f"Step {frame_idx + 1} (Permuting layer {permuted_idx} )")
            else: 
                ax.set_title(f"Step {frame_idx + 1} (To permute layer {permuted_idx} )")
        ani = FuncAnimation(fig, update, frames=len(self.snapshots), interval=delay)

        # Save to MP4 using FFMpeg
        writer = FFMpegWriter(fps=1000 // delay)
        ani.save(filename, writer=writer)
        print(f"Saved animation to {filename}")
    
class BarySiftingCutoffHybrid(BaseCutoffHybrid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        if phase == 'pre-cutoff':
            formatted_edges = parse_edges(edges, fixed_layer, free_layer)
            return barycenter(free_layer, fixed_layer, formatted_edges)
        elif phase == 'post-cutoff':
            return sifting(free_layer, fixed_layer, edges, direction)
        else:
            raise ValueError("Invalid phase argument.")
        
class PermuSiftingCutoffHybrid(BaseCutoffHybrid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        if phase == 'pre-cutoff':
            reordered_layer, _ = permutation(fixed_layer, free_layer, edges)
            return reordered_layer
        elif phase == 'post-cutoff':
            return sifting(free_layer, fixed_layer, edges, direction)
        else:
            raise ValueError("Invalid phase argument.")
    
class PermuBaryCutoffHybrid(BaseCutoffHybrid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        if phase == 'pre-cutoff':
            return sifting(free_layer, fixed_layer, edges, direction)
        elif phase == 'post-cutoff':
            formatted_edges = parse_edges(edges, fixed_layer, free_layer)
            return barycenter(free_layer, fixed_layer, formatted_edges)
        else:
            raise ValueError("Invalid phase argument.")

class BaryPermuCutoffHybrid(BaseCutoffHybrid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        if phase == 'pre-cutoff':
            formatted_edges = parse_edges(edges, fixed_layer, free_layer)
            return barycenter(free_layer, fixed_layer, formatted_edges)
        elif phase == 'post-cutoff':
            reordered_layer, _ = permutation(fixed_layer, free_layer, edges)
            return reordered_layer
        else:
            raise ValueError("Invalid phase argument.")

class SiftingPermuCutoffHybrid(BaseCutoffHybrid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
    def reorder_layer(self, free_layer, fixed_layer, edges, phase, direction):
        if phase == 'pre-cutoff':
            return sifting(free_layer, fixed_layer, edges, direction)
        elif phase == 'post-cutoff':
            reordered_layer, _ = permutation(fixed_layer, free_layer, edges)
            return reordered_layer
        else:
            raise ValueError("Invalid phase argument.")
   
if __name__ == "__main__":
    k = 10
    n = 7
    m = 7
    nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, m)
    
    x = total_crossing_count_k_layer(layers, edges)
    print("Original graph " + str(x))
    
    parsed_data = BaseCutoffHybrid.parse_layers_edges(layers, edges)
    
    #uncommented barysift
    # bary_sift = BarySiftingCutoffHybrid(layers, edges, l_cutoff=2, parsed_layer_edge_data=parsed_data, comment_out=0, capture = 1)
    # barysift_reordered,_ = bary_sift.execute()
    # barysift_reordered_count = total_crossing_count_k_layer(barysift_reordered, edges)
    # print(f"Uncommented BarycenterSifting {barysift_reordered_count}")
    
    # #commented barysift
    # bary_sifter = BarySiftingCutoffHybrid(layers, edges, l_cutoff=2, parsed_layer_edge_data=parsed_data, comment_out=1, capture = 1)
    # barysift_reordereder,_ = bary_sifter.execute()
    # barysift_reordered_counter = total_crossing_count_k_layer(barysift_reordereder, edges)
    # print(f"BarycenterSifting {barysift_reordered_counter}")

    # siftbary = SiftingBaryCutoffHybrid(layers, edges, l_cutoff=2, parsed_layer_edge_data=parsed_data, comment_out=1)
    # siftbary_reorder = siftbary.execute()
    # siftbary_reorder_counter = total_crossing_count_k_layer(siftbary_reorder, edges)
    # print(f"SiftBary {siftbary_reorder_counter}")
    permusifting = PermuSiftingCutoffHybrid(layers, edges, l_cutoff=9, parsed_layer_edge_data=parsed_data, comment_out=1, capture=1)
    start = time.perf_counter()
    permusifting_reorderer, _ = permusifting.execute()
    end = time.perf_counter()
    permusifting_reordered_counter = total_crossing_count_k_layer(permusifting_reorderer, edges)
    print(f"Permusifting {permusifting_reordered_counter}")
    print(f"time elapsed {end-start}")
    # permubary = PermuBaryCutoffHybrid(layers, edges, l_cutoff=9, parsed_layer_edge_data=parsed_data, comment_out=1)
    # permubary_reorderer, _ = permubary.execute()
    # permubary_reordered_counter = total_crossing_count_k_layer(permubary_reorderer, edges)
    # print(f"Permubary {permubary_reordered_counter}")
    
    # purepermu = PermuBaryCutoffHybrid(layers, edges, l_cutoff=k-1, parsed_layer_edge_data=parsed_data, comment_out=1, capture=0)
    # purepermu_reorderer = purepermu.execute()
    # purepermu_reordered_counter = total_crossing_count_k_layer(purepermu_reorderer, edges)
    # print(f"Pure Permu {purepermu_reordered_counter}")
    
    # purepermuonesweep = PermuBaryCutoffHybrid(layers, edges, l_cutoff=k-1, parsed_layer_edge_data=parsed_data, comment_out=1, capture=0)
    # purepermuonesweep_reorder = purepermuonesweep.execute_onesweep()
    # purepermuonesweep_counter = total_crossing_count_k_layer(purepermuonesweep_reorder, edges)
    # print(f"One pass pure permu {purepermu_reordered_counter}")
    ########## ANIMATION 
    ### may bug, the cut-off layer just oscillates kapag post-cutoff phase na
    ### new update, added the comment_out for this
    # bary_sift.animate_snapshots() # for observing the behavior
    # bary_sifter.animate_snapshots(0.1)
    # bary_sift.create_animation(filename='barysift_old_imple.mp4')
    # bary_sifter.create_animation(filename='barysift_new_imple.mp4')
    # bary_sift.create_animation(filename='barysift_old_imple.mp4')
    permusifting.create_animation(filename='permusifting_new_imple.mp4')