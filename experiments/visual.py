import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np

# Get all summary CSV files
csv_files = sorted(glob.glob("summary_*.csv"))

for file in csv_files:
    # Extract graph size from filename (e.g., "summary_10×10.csv" → "10×10")
    graph_size = file.split("_")[-1].replace(".csv", "")

    # Read CSV file
    df = pd.read_csv(file)

    # Get the highest reduction percentage (to adjust Y-axis dynamically)
    max_reduction = max(df["sifting_reduction"].max(), df["median_reduction"].max(), df["barycenter_reduction"].max())
    min_reduction = min(df["sifting_reduction"].min(), df["median_reduction"].min(), df["barycenter_reduction"].min())

    # Adjust Y-axis limit (round to nearest 5%)
    y_min = max(0, min_reduction - 2)  # Start a little lower
    y_max = np.ceil(max_reduction / 5) * 5  # Round to nearest multiple of 5 for readability

    # Plot settings
    plt.figure(figsize=(8, 5))
    
    # Line plots with thinner lines and smaller markers
    plt.plot(df["density"], df["sifting_reduction"], marker="o", linestyle="-", linewidth=.75, markersize=2, label="Sifting", color="green")
    plt.plot(df["density"], df["median_reduction"], marker="s", linestyle="--", linewidth=.75, markersize=2, label="Median", color="orange")
    plt.plot(df["density"], df["barycenter_reduction"], marker="d", linestyle="-.", linewidth=.75, markersize=2, label="Barycentric", color="blue")

    # Add labels at key points (small and subtle)
    # for i in range(len(df)):
    #     plt.text(df["density"].iloc[i], df["sifting_reduction"].iloc[i] + 0.5, f"{df['sifting_reduction'].iloc[i]:.1f}%", fontsize=8, color="green", ha='right')
    #     plt.text(df["density"].iloc[i], df["median_reduction"].iloc[i] - 0.5, f"{df['median_reduction'].iloc[i]:.1f}%", fontsize=8, color="orange", ha='left')
    #     plt.text(df["density"].iloc[i], df["barycenter_reduction"].iloc[i] + 0.5, f"{df['barycenter_reduction'].iloc[i]:.1f}%", fontsize=8, color="blue", ha='left')

    # Labels and formatting
    plt.xlabel("Graph Density")
    plt.ylabel("Reduction in Crossings (%)")
    plt.title(f"Crossing Reduction for {graph_size} Graphs")
    plt.xticks(df["density"])  # Set X-axis labels to density values
    plt.ylim(y_min, y_max)  # Dynamically adjust Y-axis
    plt.legend()
    plt.grid(True, linestyle="--", linewidth=0.5)

    # Save as PNG
    plt.savefig(f"{graph_size}_reduction.png", dpi=300)
    plt.close()  # Close the figure to avoid overlap

print("Line graph PNG files with thinner lines generated successfully!")
