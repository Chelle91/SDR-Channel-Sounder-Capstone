import os
import numpy as np
import matplotlib.pyplot as plt

# =========================
# Configuration
# =========================
fs = 250e3
tx_file = "pn.dat"
rx_file = "rx_pn.dat"

# Display window around main peak
display_window_samples = 1000

# Metric gate around peak
# At fs = 250 kHz, 1 sample = 4 us
# 50 samples = +/-200 us around detected peak
metric_gate_samples = 50

smooth_len = 5
threshold_db = -15

output_prefix = "v6b"

# =========================
# Load data
# =========================
tx = np.fromfile(tx_file, dtype=np.complex64)
rx = np.fromfile(rx_file, dtype=np.complex64)

print("TX samples:", len(tx))
print("RX samples:", len(rx))

# =========================
# Preprocessing
# =========================
tx = tx - np.mean(tx)
rx = rx - np.mean(rx)

tx = tx / (np.std(tx) + 1e-12)
rx = rx / (np.std(rx) + 1e-12)

# =========================
# Full matched-filter correlation
# =========================
corr = np.abs(np.correlate(rx, tx, mode="full"))
corr = corr / (np.max(corr) + 1e-12)

peak_index = np.argmax(corr)
peak_value = corr[peak_index]
mean_floor = np.mean(corr)
peak_to_mean = peak_value / (mean_floor + 1e-12)

print("Peak index:", peak_index)
print("Peak value:", peak_value)
print("Mean floor:", mean_floor)
print("Peak-to-mean ratio:", peak_to_mean)

# =========================
# Display window
# =========================
display_start = max(0, peak_index - display_window_samples)
display_end = min(len(corr), peak_index + display_window_samples)

display_corr = corr[display_start:display_end]
display_corr = display_corr / (np.max(display_corr) + 1e-12)

display_lags = np.arange(display_start, display_end) - peak_index
display_time_us = display_lags * (1e6 / fs)
display_db = 20 * np.log10(display_corr + 1e-12)

kernel = np.ones(smooth_len) / smooth_len
display_smooth = np.convolve(display_corr, kernel, mode="same")
display_smooth = display_smooth / (np.max(display_smooth) + 1e-12)

# =========================
# Gated metric window
# =========================
gate_start = max(0, peak_index - metric_gate_samples)
gate_end = min(len(corr), peak_index + metric_gate_samples + 1)

gate_corr = corr[gate_start:gate_end]
gate_corr = gate_corr / (np.max(gate_corr) + 1e-12)

gate_lags = np.arange(gate_start, gate_end) - peak_index
gate_time_us = gate_lags * (1e6 / fs)
gate_db = 20 * np.log10(gate_corr + 1e-12)

# Use threshold inside gated window
mask = gate_db >= threshold_db

if np.any(mask):
    p = gate_corr[mask] ** 2
    t = gate_time_us[mask]

    p_sum = np.sum(p) + 1e-12
    mean_delay_us = np.sum(t * p) / p_sum
    rms_delay_us = np.sqrt(np.sum(((t - mean_delay_us) ** 2) * p) / p_sum)

    excess_delay_us = np.max(t) - np.min(t)

    print(f"Metric gate: +/- {metric_gate_samples} samples")
    print(f"Metric gate: +/- {metric_gate_samples * (1e6/fs)} us")
    print(f"Threshold used for gated delay spread: {threshold_db} dB")
    print("Gated mean delay (us):", mean_delay_us)
    print("Gated RMS delay spread (us):", rms_delay_us)
    print("Gated excess delay span (us):", excess_delay_us)
else:
    mean_delay_us = None
    rms_delay_us = None
    excess_delay_us = None
    print("No gated samples above threshold.")

# =========================
# Save metrics
# =========================
with open(f"cir_metrics_{output_prefix}.txt", "w") as f:
    f.write(f"TX samples: {len(tx)}\n")
    f.write(f"RX samples: {len(rx)}\n")
    f.write(f"Peak index: {peak_index}\n")
    f.write(f"Peak value: {peak_value}\n")
    f.write(f"Mean floor: {mean_floor}\n")
    f.write(f"Peak-to-mean ratio: {peak_to_mean}\n")
    f.write(f"Metric gate samples: +/- {metric_gate_samples}\n")
    f.write(f"Metric gate us: +/- {metric_gate_samples * (1e6/fs)}\n")
    f.write(f"Threshold used for gated delay spread: {threshold_db} dB\n")

    if mean_delay_us is not None:
        f.write(f"Gated mean delay (us): {mean_delay_us}\n")
        f.write(f"Gated RMS delay spread (us): {rms_delay_us}\n")
        f.write(f"Gated excess delay span (us): {excess_delay_us}\n")

# =========================
# Plot 1: Full Correlation
# =========================
plt.figure(figsize=(10, 5))
plt.plot(corr)
plt.axvline(peak_index, linestyle="--")
plt.title("Full PN Correlation")
plt.xlabel("Lag Sample")
plt.ylabel("Normalized Magnitude")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"full_pn_correlation_{output_prefix}.png", dpi=300)
plt.show()

# =========================
# Plot 2: Zoomed CIR
# =========================
plt.figure(figsize=(10, 5))
plt.plot(display_time_us, display_corr)
plt.axvline(0, linestyle="--", label="Detected LOS peak")
plt.axvspan(
    -metric_gate_samples * (1e6/fs),
    metric_gate_samples * (1e6/fs),
    alpha=0.15,
    label="Metric gate"
)
plt.title("Zoomed Channel Impulse Response")
plt.xlabel("Relative Delay (µs)")
plt.ylabel("Normalized Magnitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"zoomed_cir_{output_prefix}.png", dpi=300)
plt.show()

# =========================
# Plot 3: Lightly Smoothed CIR
# =========================
plt.figure(figsize=(10, 5))
plt.plot(display_time_us, display_smooth)
plt.axvline(0, linestyle="--", label="Detected LOS peak")
plt.axvspan(
    -metric_gate_samples * (1e6/fs),
    metric_gate_samples * (1e6/fs),
    alpha=0.15,
    label="Metric gate"
)
plt.title("Lightly Smoothed CIR for Visualization")
plt.xlabel("Relative Delay (µs)")
plt.ylabel("Normalized Magnitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"smoothed_cir_{output_prefix}.png", dpi=300)
plt.show()

# =========================
# Plot 4: CIR in dB
# =========================
plt.figure(figsize=(10, 5))
plt.plot(display_time_us, display_db)
plt.axvline(0, linestyle="--", label="Detected LOS peak")
plt.axhline(threshold_db, linestyle=":", label=f"{threshold_db} dB threshold")
plt.axvspan(
    -metric_gate_samples * (1e6/fs),
    metric_gate_samples * (1e6/fs),
    alpha=0.15,
    label="Metric gate"
)
plt.title("Zoomed CIR in dB")
plt.xlabel("Relative Delay (µs)")
plt.ylabel("Magnitude (dB)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"zoomed_cir_db_{output_prefix}.png", dpi=300)
plt.show()

print("Saved:")
print(f" - full_pn_correlation_{output_prefix}.png")
print(f" - zoomed_cir_{output_prefix}.png")
print(f" - smoothed_cir_{output_prefix}.png")
print(f" - zoomed_cir_db_{output_prefix}.png")
print(f" - cir_metrics_{output_prefix}.txt")

# =========================
# Export numeric CIR data for overlays/comparisons
# =========================
np.savetxt(
    f"cir_data_{output_prefix}.csv",
    np.column_stack((display_time_us, display_corr, display_db, display_smooth)),
    delimiter=",",
    header="relative_delay_us,normalized_magnitude,magnitude_db,smoothed_magnitude",
    comments=""
)

print(f" - cir_data_{output_prefix}.csv")
