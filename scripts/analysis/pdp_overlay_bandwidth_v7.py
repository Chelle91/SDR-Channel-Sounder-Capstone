import numpy as np
import matplotlib.pyplot as plt
import os

files = {
    "250 kHz": "results/bandwidth_250k_v7/cir_data_v7.csv",
    "1 MHz": "results/bandwidth_1M_v7/cir_data_v7.csv",
    "5 MHz": "results/bandwidth_5M_v7/cir_data_v7.csv",
}

output_dir = "results/pdp_v7"
os.makedirs(output_dir, exist_ok=True)

plt.figure(figsize=(10,6))

for label, path in files.items():
    if not os.path.exists(path):
        print(f"Missing: {path}")
        continue

    data = np.loadtxt(path, delimiter=",", skiprows=1)

    delay_us = data[:, 0]
    amp = data[:, 1]

    power = amp**2
    power /= np.max(power)

    power_db = 10 * np.log10(power + 1e-12)

    plt.plot(delay_us, power_db, label=label)

plt.axvline(0, linestyle="--")

plt.title("PDP Comparison Across Bandwidths")
plt.xlabel("Delay (µs)")
plt.ylabel("Power (dB)")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(f"{output_dir}/pdp_overlay_bandwidth.png", dpi=300)
plt.show()

print("Saved:", f"{output_dir}/pdp_overlay_bandwidth.png")
