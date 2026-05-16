import os
import re
import csv
import matplotlib.pyplot as plt

scenarios = [
    ("Indoor 15 ft", "results/distance_tests/indoor_15ft/cir_metrics_v6b.txt"),
    ("Outdoor LOS", "results/outdoor_tests/outdoor_los/cir_metrics_v6b.txt"),
    ("Outdoor Obstructed", "results/outdoor_tests/outdoor_obstructed/cir_metrics_v6b.txt"),
]

def extract_metric(text, key):
    match = re.search(rf"{re.escape(key)}:\s*([-+]?\d*\.?\d+)", text)
    return float(match.group(1)) if match else None

labels = []
peak_ratios = []
rms_spreads = []
mean_floors = []
mean_delays = []

for label, path in scenarios:
    with open(path, "r") as f:
        content = f.read()

    labels.append(label)
    peak_ratios.append(extract_metric(content, "Peak-to-mean ratio"))
    rms_spreads.append(extract_metric(content, "Gated RMS delay spread (us)"))
    mean_floors.append(extract_metric(content, "Mean floor"))
    mean_delays.append(extract_metric(content, "Gated mean delay (us)"))

output_dir = "results/analysis/indoor_outdoor_comparison"
os.makedirs(output_dir, exist_ok=True)

def bar_plot(values, ylabel, title, filename):
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename), dpi=300)
    plt.close()

bar_plot(
    peak_ratios,
    "Peak-to-Mean Ratio",
    "Peak-to-Mean Ratio: Indoor vs Outdoor",
    "indoor_outdoor_peak_ratio.png",
)

bar_plot(
    rms_spreads,
    "RMS Delay Spread (µs)",
    "RMS Delay Spread: Indoor vs Outdoor",
    "indoor_outdoor_rms_spread.png",
)

bar_plot(
    mean_floors,
    "Mean Correlation Floor",
    "Mean Floor: Indoor vs Outdoor",
    "indoor_outdoor_mean_floor.png",
)

bar_plot(
    mean_delays,
    "Mean Delay (µs)",
    "Mean Delay: Indoor vs Outdoor",
    "indoor_outdoor_mean_delay.png",
)

csv_path = os.path.join(output_dir, "indoor_outdoor_summary.csv")

with open(csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Scenario",
        "Peak-to-Mean Ratio",
        "RMS Delay Spread (us)",
        "Mean Floor",
        "Mean Delay (us)",
    ])

    for i in range(len(labels)):
        writer.writerow([
            labels[i],
            peak_ratios[i],
            rms_spreads[i],
            mean_floors[i],
            mean_delays[i],
        ])

print("Saved:")
for file in [
    "indoor_outdoor_peak_ratio.png",
    "indoor_outdoor_rms_spread.png",
    "indoor_outdoor_mean_floor.png",
    "indoor_outdoor_mean_delay.png",
    "indoor_outdoor_summary.csv",
]:
    print(f" - {os.path.join(output_dir, file)}")
