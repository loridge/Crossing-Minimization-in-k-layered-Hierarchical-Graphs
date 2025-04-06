import sys
import os
import random
import json
import copy
import time
import math
import itertools
import pandas as pd
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from itertools import combinations, permutations
from typing import Dict, Union, List, Set
from concurrent.futures import ProcessPoolExecutor

from k_layered_heuristics import (
    hybrid_1_permu_bary,
    hybrid_1_sift_bary,
    hybrid_2
)

from k_layer_crossing import (
    total_crossing_count_k_layer,
)

from k_layered import (
    generate_k_layered_sparse_graph,
    visualize_k_layered_graph,
)

### need visualizer for results :>

num_samples = 50

k = 10
n = 8
m = 4


## need to take into account the cut off thing
for run in range(num_samples):
    nodes, edges, G, layers = generate_k_layered_sparse_graph(k, n, m)
    
    crossings_orig = total_crossing_count_k_layer(layers, edges)
    
    new_layers_hybrid_1_1 = hybrid_1_permu_bary(layers, edges)
    
    hybrid_1_1_count = total_crossing_count_k_layer(new_layers_hybrid_1_1, edges)
    
    
    new_layers_hybrid_1_2 = hybrid_1_sift_bary(layers, edges)
    
    hybrid_1_2_count = total_crossing_count_k_layer(new_layers_hybrid_1_2, edges)
    
    for cutoff in range(0, k):
        new_layers_hybrid_2 = hybrid_2(layers, edges, cutoff)
    
        hybrid_2_count = total_crossing_count_k_layer(new_layers_hybrid_2, edges)
