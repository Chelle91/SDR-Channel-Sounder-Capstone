import numpy as np
import matplotlib.pyplot as plt

# Load your CIR CSV (pick one scenario to start)
data = np.loadtxt("results/bandwidth_250k_v7/cir_data_v7.csv", delimiter=",", skiprows=1)

delay_us = data[:, 0]
amplitude = data[:, 1]

# Compute PDP (power)
power = amplitude ** 2

# Normalize
power /= np.max(power)

power_db = 10 * np.log10(power + 1e-12)

plt.figure(figsize=(10,6))

plt.plot(delay_us, power_db)
plt.axvline(0, linestyle="--")

plt.title("Power Delay Profile (PDP)")
plt.xlabel("Delay (µs)")
plt.ylabel("Power (dB)")
plt.grid(True)

plt.savefig("results/pdp_v7.png", dpi=300)
plt.show()

print("Saved: results/pdp_v7.png")
