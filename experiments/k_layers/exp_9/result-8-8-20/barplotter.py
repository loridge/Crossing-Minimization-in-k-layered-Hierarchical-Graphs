import pandas as pd
import matplotlib.pyplot as plt
import re

# Load your CSV
df = pd.read_csv('exp-9_timings_produced_8-8.csv')  # replace with your actual file

# Extract relevant column patterns
pattern = re.compile(r'(\w+_\w+)_cutoff_(\d+)_(total|algo1|algo2)')

# Create a mapping: algorithm -> {cutoff -> {type: value}}
algorithms = {}

# Only use first row assuming sample_id is the only row needed
row = df.iloc[0]

for col, val in row.items():
    match = pattern.match(col)
    if match:
        algo, cutoff, val_type = match.groups()
        cutoff = int(cutoff)
        if algo not in algorithms:
            algorithms[algo] = {}
        if cutoff not in algorithms[algo]:
            algorithms[algo][cutoff] = {}
        algorithms[algo][cutoff][val_type] = val

# Plot for each algorithm
for algo, cutoffs in algorithms.items():
    labels = sorted(cutoffs.keys())
    totals = [cutoffs[c]['total'] for c in labels]
    algo1s = [cutoffs[c]['algo1'] for c in labels]
    algo2s = [cutoffs[c]['algo2'] for c in labels]

    x = range(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar([i - width for i in x], totals, width, label='total')
    ax.bar(x, algo1s, width, label='algo1')
    ax.bar([i + width for i in x], algo2s, width, label='algo2')

    ax.set_title(f'Performance of {algo}')
    ax.set_xlabel('Cutoff')
    ax.set_ylabel('Value')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'{algo}_performance.png')  # Saves each graph to a file
    plt.show()
