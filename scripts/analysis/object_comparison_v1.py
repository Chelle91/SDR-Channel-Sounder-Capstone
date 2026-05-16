import os
import re
import csv
import matplotlib.pyplot as plt

base_dir = "results/object_tests"

scenarios = [
    "baseline_los",
    "cardboard_obstruction",
    "wood_obstruction",
    "human_obstruction",
    "aluminum_obstruction"
]

labels = [
    "Baseline LOS",
    "Cardboard",
    "Wood",
    "Human",
    "Aluminum"
]

peak_ratios = []
rms_spreads = []
mean_floors = []

def extract_metric(text, key):
    match = re.search(rf"{re.escape(key)}:\s*([-+]?\d*\.?\d+)", text)
    if match:
        return float(match.group(1))
    return None

for scenario in scenarios:
    metrics_path = os.path.join(
        base_dir,
        scenario,
        "cir_metrics_v6b.txt"
    )

    with open(metrics_path, "r") as f:
        content = f.read()

    peak_ratio = extract_metric(content, "Peak-to-mean ratio")
    rms_spread = extract_metric(content, "Gated RMS delay spread (us)")
    mean_floor = extract_metric(content, "Mean floor")

    peak_ratios.append(peak_ratio)
    rms_spreads.append(rms_spread)
    mean_floors.append(mean_floor)

output_dir = "results/analysis/object_comparison"
os.makedirs(output_dir, exist_ok=True)

# Peak ratio plot
plt.figure(figsize=(8,5))
plt.bar(labels, peak_ratios)
plt.ylabel("Peak-to-Mean Ratio")
plt.title("Peak-to-Mean Ratio by Object")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(f"{output_dir}/object_peak_ratio.png")
plt.close()

# RMS spread plot
plt.figure(figsize=(8,5))
plt.bar(labels, rms_spreads)
plt.ylabel("RMS Delay Spread (µs)")
plt.title("RMS Delay Spread by Object")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(f"{output_dir}/object_rms_spread.png")
plt.close()

# Mean floor plot
plt.figure(figsize=(8,5))
plt.bar(labels, mean_floors)
plt.ylabel("Mean Correlation Floor")
plt.title("Mean Floor by Object")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(f"{output_dir}/object_mean_floor.png")
plt.close()

# Save summary CSV
csv_path = f"{output_dir}/object_summary.csv"

with open(csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow([
        "Scenario",
        "Peak-to-Mean Ratio",
        "RMS Delay Spread (us)",
        "Mean Floor"
    ])

    for i in range(len(labels)):
        writer.writerow([
            labels[i],
            peak_ratios[i],
            rms_spreads[i],
            mean_floors[i]
        ])

print("Saved:")
print(f" - {output_dir}/object_peak_ratio.png")
print(f" - {output_dir}/object_rms_spread.png")
print(f" - {output_dir}/object_mean_floor.png")
print(f" - {output_dir}/object_summary.csv")
