import numpy as np
import matplotlib.pyplot as plt
import os

# =========================
# Input RMS delay spreads (µs)
# Use values from v6b
# =========================

scenarios = {
    "Baseline LOS": 98,
    "LOS 3 ft": 113,
    "LOS 5.25 ft": 120,
    "NLOS": 110,
}

os.makedirs("results/coherence_v7", exist_ok=True)

labels = []
bc_values = []

print("\n=== Coherence Bandwidth Estimates ===")

for label, tau_us in scenarios.items():
    tau_s = tau_us * 1e-6
    bc = 1 / (5 * tau_s)

    labels.append(label)
    bc_values.append(bc / 1e3)  # convert to kHz

    print(f"{label}: τ_rms = {tau_us} µs → Bc ≈ {bc/1e3:.2f} kHz")

# =========================
# Plot
# =========================

plt.figure(figsize=(10,6))
plt.bar(labels, bc_values)

plt.title("Estimated Coherence Bandwidth by Scenario")
plt.ylabel("Coherence Bandwidth (kHz)")
plt.xlabel("Scenario")
plt.grid(axis='y')

plt.tight_layout()
plt.savefig("results/coherence_v7/coherence_bandwidth.png", dpi=300)
plt.show()

# =========================
# Save CSV
# =========================

with open("results/coherence_v7/coherence_bandwidth.csv", "w") as f:
    f.write("Scenario,Coherence_Bandwidth_kHz\n")
    for label, val in zip(labels, bc_values):
        f.write(f"{label},{val}\n")

print("\nSaved:")
print(" - results/coherence_v7/coherence_bandwidth.png")
print(" - results/coherence_v7/coherence_bandwidth.csv")
