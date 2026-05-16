import os
import numpy as np
import matplotlib.pyplot as plt

files = {
    "250 kHz": ("results/bandwidth_250k_v7/cir_data_v7.csv", 250e3),
    "1 MHz": ("results/bandwidth_1M_v7/cir_data_v7.csv", 1e6),
    "5 MHz": ("results/bandwidth_5M_v7/cir_data_v7.csv", 5e6),
}

output_dir = "results/lightweight_fft_frequency_response"
os.makedirs(output_dir, exist_ok=True)

plt.figure(figsize=(10, 6))

for label, (path, fs) in files.items():
    if not os.path.exists(path):
        print(f"Missing file: {path}")
        continue

    data = np.loadtxt(path, delimiter=",", skiprows=1)

    # Columns: delay_us, normalized_magnitude, magnitude_db
    h = data[:, 1]

    # Remove DC and apply window to reduce FFT artifacts
    h = h - np.mean(h)
    window = np.hanning(len(h))
    h_win = h * window

    # FFT of CIR gives estimated frequency response
    H = np.fft.fftshift(np.fft.fft(h_win))
    freq = np.fft.fftshift(np.fft.fftfreq(len(h_win), d=1/fs))

    H_mag_db = 20 * np.log10(np.abs(H) / (np.max(np.abs(H)) + 1e-12) + 1e-12)

    plt.plot(freq / 1e6, H_mag_db, label=label)

plt.title("Lightweight FFT-Based Frequency Response Estimate")
plt.xlabel("Baseband Frequency Offset (MHz)")
plt.ylabel("Normalized Magnitude (dB)")
plt.grid(True)
plt.legend()
plt.tight_layout()

out_file = os.path.join(output_dir, "frequency_response_overlay.png")
plt.savefig(out_file, dpi=300)
plt.show()

print("Saved:", out_file)
