import pandas as pd
import glob

# Get all experiment CSV files (e.g., exp2_results_10+10.csv, ..., 50+50)
csv_files = sorted(glob.glob("exp2_results_*.csv"))

for file in csv_files:
    # Extract graph size (e.g., "exp2_results_10+10.csv" → "10×10")
    graph_size = file.split("_")[-1].replace(".csv", "").replace("+", "×")

    # Read CSV
    df = pd.read_csv(file)

    # Compute percentage reductions and round them
    for heuristic in ["sifting", "median", "barycenter"]:
        col_name = f"avg_crossings_{heuristic}"
        if col_name in df.columns:
            df[f"{heuristic}_reduction"] = ((df["avg_crossings_original"] - df[col_name]) / df["avg_crossings_original"]) * 100
            df[f"{heuristic}_reduction"] = df[f"{heuristic}_reduction"].round(3)  # Round to 1 decimal place

    # Keep only necessary columns
    summary_df = df[["density", "avg_crossings_original", "sifting_reduction", "median_reduction", "barycenter_reduction"]]

    # Save the summary CSV for this graph type
    summary_df.to_csv(f"summary_{graph_size}.csv", index=False)

print("Summary CSV files with rounded percentages generated successfully!")