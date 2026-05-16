import os
import csv
import numpy as np
import matplotlib.pyplot as plt

scenarios = [
    ("Indoor 15 ft", "results/distance_tests/indoor_15ft/cir_data_v6b.csv"),
    ("Outdoor LOS", "results/outdoor_tests/outdoor_los/cir_data_v6b.csv"),
    ("Outdoor Obstructed", "results/outdoor_tests/outdoor_obstructed/cir_data_v6b.csv"),
]

output_dir = "results/analysis/final_overlays"
os.makedirs(output_dir, exist_ok=True)

plt.figure(figsize=(10, 6))

window = 15

for label, path in scenarios:
    x = []
    y = []

    with open(path, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            x.append(float(row["relative_delay_us"]))
            y.append(float(row["normalized_magnitude"]))

    x = np.array(x)
    y = np.array(y)

    # Moving-average smoothing
    kernel = np.ones(window) / window
    y_smooth = np.convolve(y, kernel, mode='same')

    plt.plot(
        x,
        y_smooth,
        linewidth=2,
        label=label
    )

plt.title("Smoothed CIR Overlay Across Final Environments")
plt.xlabel("Relative Delay (µs)")
plt.ylabel("Normalized Magnitude")
plt.xlim([-4000, 4000])
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    f"{output_dir}/final_environment_overlay_smoothed.png",
    dpi=300
)

plt.close()

print("Saved:")
print(f" - {output_dir}/final_environment_overlay_smoothed.png")
