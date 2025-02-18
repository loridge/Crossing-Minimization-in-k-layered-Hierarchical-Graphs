from bipartite_graph_generator import generate_bipartite_graph, visualize_bipartite_graph, count_crossings, update_positions, plot_results
from two_layer_barycenter import barycenter, parse_edges, median, draw_horizontal_bipartite
from edgedensity import generator_bip_graph
from sifting_2 import sifting
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from crossing_func import cross_count
# Parameters for experimentation
n1_values = [5] # Top-layer node counts
n2_values = [5]  # Bottom-layer node counts
p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]  # Edge probabilities
# p_values = [0.1]
# Results list to store experiment outcomes
results = []
graphs = []

# Start the timer
start_time = time.time()

# Experiment loop
for n1 in n1_values:
    for n2 in n2_values:
        for p in p_values:
            # Generate bipartite graph
            # nodes, edges, B, top_nodes, bottom_nodes = generate_bipartite_graph(n1, n2, p)
            nodes, edges, B, top_nodes, bottom_nodes = generator_bip_graph(n1, n2, p, LA=1)
            # print("generated lauers", top_nodes, bottom_nodes)
            # Calculate density, not yet bipartite
            # density = nx.density(B)
            density = bipartite.density(B, set(top_nodes))
            # Visualize the graph (optional, for small graphs)
            #visualize_bipartite_graph(B, bottom_nodes)
            
            # Original layout
            pos_original = nx.bipartite_layout(B, top_nodes, align="horizontal")
            # print("pos original",pos_original)
            crossings_original = count_crossings(B, pos_original)

            # Parse the edges into (top_node, bottom_node) tuples before passing to the barycenter function
            parsed_edges = parse_edges(edges, top_nodes, bottom_nodes)
            
            # Apply Barycenter heuristic to reorder bottom nodes
            bottom_nodes_bary = barycenter(bottom_nodes, top_nodes, parsed_edges)

            #visualize_bipartite_graph(B, bottom_nodes_bary)

            # Update positions: top nodes fixed, bottom nodes reordered
            pos_barycenter = update_positions(top_nodes, bottom_nodes_bary)
            crossings_barycenter = count_crossings(B, pos_barycenter)
            
            # Apply Median heuristic to reorder bottom nodes
            bottom_nodes_median = median(bottom_nodes, top_nodes, parsed_edges)

            # Update positions: top nodes fixed, bottom nodes reordered
            pos_median = update_positions(top_nodes, bottom_nodes_median)
            # print("POS_MEDIAN", pos_median) #LELEY nilagay ko to
            crossings_median = count_crossings(B, pos_median)

            #visualize_bipartite_graph(B, bottom_nodes_median)

            # Apply Simple Sifting heuristic to reorder bottom nodes
            # does not accept edges as tuples
            sifting_heuristic = sifting(bottom_nodes, top_nodes, edges, verbose=0, LA_gen=1)

            # draw_horizontal_bipartite(B, top_nodes, sifting_heuristic, "After Sift Algorithm") ## bug spotted, i also commented a code out in sifting
            #LELEY inedit ko draw_horiz_bipartite, sifting ---> sifting_heuristics
            pos_sifting = update_positions(top_nodes, sifting_heuristic) # the sifting_heuristic is 1,2,3,4,5 while the previous ones have 'u1, u2,..' 
            # leley ninote ko lang yung pagdebug ko
            
            # print("POS_SIFTING", pos_sifting)
            
            # crossings_sifting = count_crossings(B, pos_sifting)
            crossings_sifting = cross_count(top_nodes, sifting_heuristic, edges, LA_gen=1)
            # Store results
            results.append({
                "n1": n1,
                "n2": n2,
                "p": p,
                "density": density,
                "crossings_original": crossings_original,
                "crossings_barycenter": crossings_barycenter,
                "crossings_median": crossings_median,
                "crossings_sifting": crossings_sifting
            })

            # Store the graph and positions for plotting
            graphs.append((B, pos_original, pos_barycenter, pos_median, pos_sifting))

# End the timer and print the total execution time
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

def plot_all_graphs(graphs):
    """
    Plots all the generated bipartite graphs in a grid of subplots.
    
    Args:
        graphs (list): List of tuples containing the graph and positions for each layout.
    """
    if not graphs:
        print("No graphs to plot.")
        return

    num_graphs = len(graphs)
    fig, axes = plt.subplots(num_graphs, 4, figsize=(20, 4 * num_graphs))

    for i, (B, pos_original, pos_barycenter, pos_median, pos_sifting) in enumerate(graphs):
        # Plot original layout
        nx.draw(B, pos_original, ax=axes[i, 0], with_labels=True, node_size=300, node_color='lightblue', edge_color='gray')
        axes[i, 0].set_title(f'Original (p={p_values[i]})')

        # Plot Barycenter layout
        nx.draw(B, pos_barycenter, ax=axes[i, 1], with_labels=True, node_size=300, node_color='lightgreen', edge_color='gray')
        axes[i, 1].set_title('Barycenter')

        # Plot Median layout
        nx.draw(B, pos_median, ax=axes[i, 2], with_labels=True, node_size=300, node_color='lightcoral', edge_color='gray')
        axes[i, 2].set_title('Median')

        # Plot Sifting layout
        nx.draw(B, pos_sifting, ax=axes[i, 3], with_labels=True, node_size=300, node_color='lightyellow', edge_color='gray')
        axes[i, 3].set_title('Sifting')

    plt.tight_layout()

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Bipartite Graphs")

    # Create a canvas widget
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add vertical and horizontal scrollbars to the canvas
    v_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    h_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Create a frame inside the canvas
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Add the Matplotlib figure to the frame
    canvas_agg = FigureCanvasTkAgg(fig, frame)
    canvas_agg.draw()
    canvas_agg.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Update the scroll region
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Start the Tkinter main loop
    root.mainloop()

# Plot all generated bipartite graphs
plot_all_graphs(graphs)
