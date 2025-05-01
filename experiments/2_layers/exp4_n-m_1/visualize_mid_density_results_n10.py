import pandas as pd
import matplotlib.pyplot as plt
import os

folder_path = "experiments/2_layers/exp4_n-m_1/"  # Path to the folder containing CSV files
os.chdir(folder_path)  # Change to the folder path

# Limited list of m values for n=10 (using fewer values for simplicity)
m_values = [5, 6, 7, 8, 9, 10]  # Example m values for n=10

# Define the target mid-density value (around 0.5)
mid_density = 0.5
tolerance = 0.05  

# Prepare a dictionary to store the results for each m combination
results = {m: {'barycenter': [], 'sifting': [], 'optimal': [], 'median': []} for m in m_values}

# Read CSV files for each combination (e.g., 10+5, 10+6, ...)
for m in m_values:
    file_name = f'exp4_results_10+{m}.csv'  # Example: crossing_reductions_10_5.csv
    try:
        df = pd.read_csv(file_name)
        
        # Filter the data for mid-density (around 0.5)
        df_filtered = df[(df['density'] >= mid_density - tolerance) & (df['density'] <= mid_density + tolerance)]
        
        # Collect crossings for each heuristic for the filtered density range
        for index, row in df_filtered.iterrows():
            # Calculate the solution quality as a percentage with respect to the optimal heuristic
            barycenter_quality = (row['avg_crossings_barycenter'] / row['avg_crossings_optimal']) * 100
            median_quality = (row['avg_crossings_median'] / row['avg_crossings_optimal']) * 100
            sifting_quality = (row['avg_crossings_sifting'] / row['avg_crossings_optimal']) * 100
            optimal_quality = (row['avg_crossings_optimal'] / row['avg_crossings_optimal']) * 100  # Always 100%

            results[m]['barycenter'].append(barycenter_quality)
            results[m]['median'].append(median_quality)
            results[m]['sifting'].append(sifting_quality)
            results[m]['optimal'].append(optimal_quality)
    except FileNotFoundError:
        print(f"Warning: {file_name} not found. Skipping.")

# Create the plot
plt.figure(figsize=(10, 6))

# Plot the results for each heuristic across all m values
# Use a single line and marker for each heuristic
plt.plot(m_values, [results[m]['barycenter'][-1] for m in m_values], label="Barycenter", marker='o', linestyle='-', markersize=6)
plt.plot(m_values, [results[m]['sifting'][-1] for m in m_values], label="Sifting", marker='^', linestyle='-', markersize=6)
plt.plot(m_values, [results[m]['median'][-1] for m in m_values], label="Median", marker='x', linestyle='-', markersize=6)
plt.plot(m_values, [results[m]['optimal'][-1] for m in m_values], label="Optimal", marker='s', linestyle='-', markersize=6)

# Customize the plot
plt.xlabel('m Value')
plt.ylabel('Solution Quality (%)')
plt.title(f"Solution Quality for Different Heuristics and m Values (n=10) \n(Filtered for Mid-Density Around {mid_density})")
plt.legend(title="Heuristics", loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)

# Save the plot in the same directory as the script
script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory where the script is located
plot_filename = os.path.join(script_dir, "vis_increasing_m_n10_mid_density.png")  # Path to save the plot

# Save and display the plot
plt.tight_layout()
plt.savefig(plot_filename, dpi=300)
plt.show()

print(f"Plot saved as '{plot_filename}'.")