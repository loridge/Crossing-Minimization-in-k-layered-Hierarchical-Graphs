import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from concurrent.futures import ProcessPoolExecutor
import time
from itertools import permutations

from bipartite_graph_generator import generate_bipartite_graph, visualize_bipartite_graph, count_crossings, update_positions, plot_results
from two_layer_barycenter import barycenter, parse_edges, median, draw_horizontal_bipartite, branch_and_cut
from edgedensity import generator_bip_graph
from sifting_2 import sifting

# Parameters for experimentation
n1_values = [40] # Top-layer node counts
n2_values = [40]  # Bottom-layer node counts
p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]  # Edge probabilities
# p_values = [0.2]
# Results list to store experiment outcomes
results = []

def run_experiment(n1, n2, p):
    # Generate bipartite graph
    # nodes, edges, B, top_nodes, bottom_nodes = generator_bip_graph(n1, n2, p)
    nodes, edges, B, top_nodes, bottom_nodes = generate_bipartite_graph(n1, n2, p)

    # Calculate density
    density = bipartite.density(B, set(top_nodes))

    # Original layout
    pos_original = nx.bipartite_layout(B, top_nodes, align="horizontal")
    crossings_original = count_crossings(B, pos_original)

    # Parse the edges into (top_node, bottom_node) tuples before passing to the barycenter function
    parsed_edges = parse_edges(edges, top_nodes, bottom_nodes)

    # Apply Barycenter heuristic to reorder bottom nodes
    bottom_nodes_bary = barycenter(bottom_nodes, top_nodes, parsed_edges)
    pos_barycenter = update_positions(top_nodes, bottom_nodes_bary)
    crossings_barycenter = count_crossings(B, pos_barycenter)

    # Apply Median heuristic to reorder bottom nodes
    bottom_nodes_median = median(bottom_nodes, top_nodes, parsed_edges)
    pos_median = update_positions(top_nodes, bottom_nodes_median)
    crossings_median = count_crossings(B, pos_median)

    # Apply Simple Sifting heuristic to reorder bottom nodes
    sifting_heuristic = sifting(bottom_nodes, top_nodes, edges, verbose=0, generated=1)
    pos_sifting = update_positions(top_nodes, sifting_heuristic)
    crossings_sifting = count_crossings(B, pos_sifting)

    # Apply Branch-and-Cut algorithm to reorder bottom nodes
    # bottom_nodes_branch_and_cut = branch_and_cut(bottom_nodes, top_nodes, edges)
    # pos_branch_and_cut = update_positions(top_nodes, bottom_nodes_branch_and_cut)
    # crossings_branch_and_cut = count_crossings(B, pos_branch_and_cut)

    return {
        "n1": n1,
        "n2": n2,
        "p": p,
        "density": density,
        "crossings_original": crossings_original,
        "crossings_barycenter": crossings_barycenter,
        "crossings_median": crossings_median,
        "crossings_sifting": crossings_sifting,
        # "crossings_branch_and_cut": crossings_branch_and_cut
    }

if __name__ == '__main__':
    # Start the timer
    start_time = time.time()

    # Experiment loop
    with ProcessPoolExecutor() as executor:
        futures = []
        for n1 in n1_values:
            for n2 in n2_values:
                for p in p_values:
                    futures.append(executor.submit(run_experiment, n1, n2, p))

        for future in futures:
            results.append(future.result())

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")
    # Convert results to a DataFrame for analysis
    df = pd.DataFrame(results)

    # Display results
    print(df)

    # Save the dataframe to a CSV file
    df.to_csv('experiment_results.csv', index=False)

    print("Results saved to 'experiment_results.csv'.")

    # Call the plot function after results are stored
    plot_results(df)