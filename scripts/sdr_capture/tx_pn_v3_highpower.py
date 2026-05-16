import numpy as np
import uhd

# =========================
# Configuration
# =========================
serial = "338D94C"      # TX device
freq = 2.45e9
rate = 250e3
gain = 80               # Increased TX power

# =========================
# Load PN sequence
# =========================
pn = np.fromfile("pn.dat", dtype=np.complex64)

# Repeat PN for continuous transmit
samples = np.tile(pn, 100).astype(np.complex64)

print("PN length:", len(pn))
print("TX buffer length:", len(samples))

# =========================
# Setup USRP
# =========================
usrp = uhd.usrp.MultiUSRP(f"serial={serial}")

usrp.set_tx_rate(rate)
usrp.set_tx_freq(uhd.types.TuneRequest(freq))
usrp.set_tx_gain(gain)

# IMPORTANT: correct antenna
usrp.set_tx_antenna("TX/RX")

# =========================
# Stream setup
# =========================
stream_args = uhd.usrp.StreamArgs("fc32", "sc16")
tx_streamer = usrp.get_tx_stream(stream_args)

metadata = uhd.types.TXMetadata()
metadata.start_of_burst = True
metadata.end_of_burst = False
metadata.has_time_spec = False

print("\n=== TX START ===")
print(f"Serial: {serial}")
print(f"Freq: {freq/1e9} GHz")
print(f"Rate: {rate/1e3} kS/s")
print(f"Gain: {gain} dB")
print("Press Ctrl+C to stop\n")

# =========================
# Transmit loop
# =========================
try:
    while True:
        sent = tx_streamer.send(samples, metadata)
        metadata.start_of_burst = False

        if sent != len(samples):
            print(f"Warning: sent {sent}/{len(samples)} samples")

except KeyboardInterrupt:
    metadata.end_of_burst = True
    tx_streamer.send(np.zeros(1000, dtype=np.complex64), metadata)
    print("\nTX stopped cleanly.")
