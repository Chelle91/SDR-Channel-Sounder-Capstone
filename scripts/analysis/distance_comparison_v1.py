import os
import re
import csv
import matplotlib.pyplot as plt

base_dir = "results/distance_tests"

scenarios = [
    "indoor_6ft",
    "indoor_10ft",
    "indoor_15ft"
]

labels = [
    "6 ft",
    "10 ft",
    "15 ft"
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

output_dir = "results/analysis/distance_comparison"
os.makedirs(output_dir, exist_ok=True)

# Peak ratio
plt.figure(figsize=(8,5))
plt.plot(labels, peak_ratios, marker='o')
plt.title("Peak-to-Mean Ratio vs Distance")
plt.ylabel("Peak-to-Mean Ratio")
plt.xlabel("Distance")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/distance_peak_ratio.png")
plt.close()

# RMS spread
plt.figure(figsize=(8,5))
plt.plot(labels, rms_spreads, marker='o')
plt.title("RMS Delay Spread vs Distance")
plt.ylabel("RMS Delay Spread (µs)")
plt.xlabel("Distance")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/distance_rms_spread.png")
plt.close()

# Mean floor
plt.figure(figsize=(8,5))
plt.plot(labels, mean_floors, marker='o')
plt.title("Mean Correlation Floor vs Distance")
plt.ylabel("Mean Correlation Floor")
plt.xlabel("Distance")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/distance_mean_floor.png")
plt.close()

# Summary CSV
csv_path = f"{output_dir}/distance_summary.csv"

with open(csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow([
        "Distance",
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
print(f" - {output_dir}/distance_peak_ratio.png")
print(f" - {output_dir}/distance_rms_spread.png")
print(f" - {output_dir}/distance_mean_floor.png")
print(f" - {output_dir}/distance_summary.csv")
