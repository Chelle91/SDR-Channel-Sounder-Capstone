import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--fs", type=float, required=True, help="Sample rate in Hz")
parser.add_argument("--label", type=str, default="channelizer")
parser.add_argument("--subbands", type=int, default=16)
parser.add_argument("--tx", type=str, default="pn.dat")
parser.add_argument("--rx", type=str, default="rx_pn.dat")
parser.add_argument("--out", type=str, default="results/fft_channelizer_v8")
args = parser.parse_args()

os.makedirs(args.out, exist_ok=True)

tx = np.fromfile(args.tx, dtype=np.complex64)
rx = np.fromfile(args.rx, dtype=np.complex64)

tx = tx - np.mean(tx)
rx = rx - np.mean(rx)

tx = tx / (np.std(tx) + 1e-12)
rx = rx / (np.std(rx) + 1e-12)

# Align RX to TX using correlation
corr = np.abs(np.correlate(rx, tx, mode="full"))
peak_index = np.argmax(corr)
lag = peak_index - (len(tx) - 1)

start = max(0, lag)
end = start + len(tx)

if end > len(rx):
    raise RuntimeError("Aligned RX segment exceeds RX length.")

rx_seg = rx[start:end]
tx_seg = tx[:len(rx_seg)]

# FFT-based channel estimate
nfft = 4096
X = np.fft.fftshift(np.fft.fft(tx_seg, n=nfft))
Y = np.fft.fftshift(np.fft.fft(rx_seg, n=nfft))
freq = np.fft.fftshift(np.fft.fftfreq(nfft, d=1/args.fs))

# Avoid divide by near-zero bins
mask = np.abs(X) > 0.05 * np.max(np.abs(X))
H = np.zeros_like(Y, dtype=np.complex128)
H[mask] = Y[mask] / X[mask]

H_mag = np.abs(H)
H_mag = H_mag / (np.max(H_mag) + 1e-12)
H_db = 20 * np.log10(H_mag + 1e-12)

# Subband averages
subband_edges = np.linspace(-args.fs/2, args.fs/2, args.subbands + 1)
subband_centers = []
subband_gain_db = []

for i in range(args.subbands):
    f0 = subband_edges[i]
    f1 = subband_edges[i + 1]
    idx = (freq >= f0) & (freq < f1) & mask

    if np.any(idx):
        gain = np.mean(H_db[idx])
    else:
        gain = np.nan

    subband_centers.append((f0 + f1) / 2)
    subband_gain_db.append(gain)

subband_centers = np.array(subband_centers)
subband_gain_db = np.array(subband_gain_db)

# Save CSV
csv_path = os.path.join(args.out, f"fft_channelizer_{args.label}.csv")
with open(csv_path, "w") as f:
    f.write("subband,center_frequency_hz,average_gain_db\n")
    for i, (fc, g) in enumerate(zip(subband_centers, subband_gain_db)):
        f.write(f"{i},{fc},{g}\n")

# Plot 1: frequency response
plt.figure(figsize=(10, 5))
plt.plot(freq / 1e6, H_db)
plt.title(f"Estimated Channel Frequency Response ({args.label})")
plt.xlabel("Baseband Frequency Offset (MHz)")
plt.ylabel("Normalized Magnitude (dB)")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(args.out, f"frequency_response_{args.label}.png"), dpi=300)
plt.show()

# Plot 2: subband gain
plt.figure(figsize=(10, 5))
plt.bar(subband_centers / 1e6, subband_gain_db, width=(args.fs / args.subbands) / 1e6 * 0.85)
plt.title(f"FFT Channelizer Sub-Band Gain ({args.label})")
plt.xlabel("Sub-Band Center Frequency (MHz)")
plt.ylabel("Average Gain (dB)")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(os.path.join(args.out, f"subband_gain_{args.label}.png"), dpi=300)
plt.show()

# Plot 3: simple heatmap view
heatmap = np.tile(subband_gain_db, (20, 1))

plt.figure(figsize=(10, 4))
plt.imshow(
    heatmap,
    aspect="auto",
    origin="lower",
    extent=[subband_centers[0]/1e6, subband_centers[-1]/1e6, 0, 1],
)
plt.colorbar(label="Average Gain (dB)")
plt.title(f"Delay-Averaged Sub-Band Channel Heatmap ({args.label})")
plt.xlabel("Baseband Frequency Offset (MHz)")
plt.yticks([])
plt.tight_layout()
plt.savefig(os.path.join(args.out, f"subband_heatmap_{args.label}.png"), dpi=300)
plt.show()

print("Saved:")
print(csv_path)
print(os.path.join(args.out, f"frequency_response_{args.label}.png"))
print(os.path.join(args.out, f"subband_gain_{args.label}.png"))
print(os.path.join(args.out, f"subband_heatmap_{args.label}.png"))
