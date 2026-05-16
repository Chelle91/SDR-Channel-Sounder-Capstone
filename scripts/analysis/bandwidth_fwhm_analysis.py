import os
import numpy as np
import matplotlib.pyplot as plt

files = {
    "250 kHz": "results/bandwidth_250k_v7/cir_data_v7.csv",
    "1 MHz": "results/bandwidth_1M_v7/cir_data_v7.csv",
    "5 MHz": "results/bandwidth_5M_v7/cir_data_v7.csv",
}

os.makedirs("results/bandwidth_comparison_v7", exist_ok=True)

def compute_fwhm(t, y):
    y = y / (np.max(y) + 1e-12)
    peak_idx = np.argmax(y)
    half_max = 0.5

    left_idx = peak_idx
    while left_idx > 0 and y[left_idx] >= half_max:
        left_idx -= 1

    right_idx = peak_idx
    while right_idx < len(y)-1 and y[right_idx] >= half_max:
        right_idx += 1

    width_us = t[right_idx] - t[left_idx]
    return width_us, t[peak_idx]

labels = []
widths = []
peak_locations = []

for label, path in files.items():
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    t = data[:, 0]
    mag = data[:, 1]
    width_us, peak_us = compute_fwhm(t, mag)

    labels.append(label)
    widths.append(width_us)
    peak_locations.append(peak_us)

    print(f"{label}: FWHM = {width_us:.3f} us, peak location = {peak_us:.3f} us")

with open("results/bandwidth_comparison_v7/fwhm_summary.csv", "w") as f:
    f.write("Bandwidth,FWHM_us,Peak_location_us\n")
    for label, width, peak in zip(labels, widths, peak_locations):
        f.write(f"{label},{width},{peak}\n")

plt.figure(figsize=(8,5))
plt.bar(labels, widths)
plt.title("CIR Peak Width vs Bandwidth")
plt.ylabel("FWHM (µs)")
plt.xlabel("Bandwidth / Sample Rate")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("results/bandwidth_comparison_v7/fwhm_vs_bandwidth.png", dpi=300)
plt.show()

print("Saved:")
print(" - results/bandwidth_comparison_v7/fwhm_vs_bandwidth.png")
print(" - results/bandwidth_comparison_v7/fwhm_summary.csv")
