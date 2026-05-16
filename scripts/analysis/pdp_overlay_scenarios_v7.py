import numpy as np
import matplotlib.pyplot as plt
import os

scenarios = {
    "Baseline LOS": "results/baseline_los_v6b/cir_data_v7.csv",
    "LOS 3 ft": "results/los_3ft_v6b/cir_data_v7.csv",
    "LOS 5.25 ft": "results/los_5p25ft_v6b/cir_data_v7.csv",
    "NLOS": "results/nlos_obstructed_v6b/cir_data_v7.csv",
}

output_dir = "results/pdp_v7"
os.makedirs(output_dir, exist_ok=True)

plt.figure(figsize=(10,6))

for label, path in scenarios.items():
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

plt.title("PDP Comparison Across Scenarios")
plt.xlabel("Delay (µs)")
plt.ylabel("Power (dB)")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(f"{output_dir}/pdp_overlay_scenarios.png", dpi=300)
plt.show()

print("Saved:", f"{output_dir}/pdp_overlay_scenarios.png")
