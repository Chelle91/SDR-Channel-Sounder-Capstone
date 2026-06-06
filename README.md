# SDR-Based Wireless Channel Sounder

## Project Overview

This project implements an SDR-based wireless channel sounder using USRP B200 software-defined radios. The system transmits a known PN sequence over the air, captures the received signal, performs cross-correlation, and extracts channel impulse response (CIR), power delay profile (PDP), and channel metrics.

The goal is to measure and visualize how wireless signals propagate in real environments, including indoor multipath, object obstruction, distance variation, and outdoor line-of-sight/non-line-of-sight behavior.

# Final Deliverables

- [Final Technical Report (PDF)](docs/final_report/SDR_Channel_Sounder_Final_Report.pdf)
- [Final Presentation](presentation/final_presentation.pdf)
- [Project Repository](.)

## Quick Links

- Experimental results: `results/`
- Signal-processing scripts: `scripts/signal_processing/`
- Analysis scripts: `scripts/analysis/`
- SDR capture scripts: `scripts/sdr_capture/`

## Repository Overview

This repository contains the complete implementation, experimentation, analysis, and documentation for an SDR-based wireless channel sounder developed using Ettus USRP B200 software-defined radios.

The project focused on extracting and analyzing wireless channel impulse responses across multiple indoor and outdoor propagation environments using pseudo-random sequence transmission, offline IQ processing, and comparative propagation analysis.

Key implemented capabilities include:

- Over-the-air SDR transmission and reception
- CIR and PDP extraction
- Indoor LOS and obstruction testing
- Outdoor propagation analysis
- Bandwidth-dependent resolution analysis
- Coherence bandwidth estimation
- FFT-based frequency-selective fading analysis
- Comparative visualization and overlay generation

## Project Status

The minimum viable product (MVP) has been completed and validated.

Completed capabilities include:

- PN waveform generation
- Over-the-air SDR transmission
- SDR receive capture
- Cross-correlation processing
- CIR extraction
- PDP generation
- RMS delay spread calculation
- Peak-to-mean ratio calculation
- Object obstruction testing
- Indoor distance sweep testing
- Outdoor LOS and obstructed testing
- Bandwidth and frequency-domain analysis
- Final comparative environment overlays

## Hardware and Software

### Hardware

- 2 × USRP B200 SDRs
- 2.4 GHz antennas
- Linux/WSL development environment

### Software

- Python 3
- NumPy
- SciPy
- Matplotlib
- UHD

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── docs/
├── presentation/
├── scripts/
│   ├── sdr_capture/
│   ├── signal_processing/
│   └── analysis/
└── results/
    ├── object_tests/
    ├── distance_tests/
    ├── outdoor_tests/
    ├── bandwidth_tests/
    ├── coherence_v7/
    └── analysis/
Main Scripts
SDR Capture
scripts/sdr_capture/make_pn_v2.py
scripts/sdr_capture/tx_pn_v3_highpower.py
Signal Processing
scripts/signal_processing/plot_cir_v6b_export_csv.py
scripts/signal_processing/pdp_plot_v7.py
scripts/signal_processing/coherence_bandwidth_v7.py
Analysis
scripts/analysis/object_comparison_v1.py
scripts/analysis/distance_comparison_v1.py
scripts/analysis/indoor_outdoor_comparison_v1.py
scripts/analysis/final_overlay_v1.py
scripts/analysis/bandwidth_fwhm_analysis.py
scripts/analysis/lightweight_fft_frequency_response.py
scripts/analysis/fft_channelizer_v8.py
scripts/analysis/pdp_overlay_scenarios_v7.py
scripts/analysis/pdp_overlay_bandwidth_v7.py
Experiments Performed
Object Obstruction Tests

Object-based tests evaluated how different materials affected the measured channel.

Scenarios:

Baseline LOS
Cardboard obstruction
Wood obstruction
Human obstruction
Aluminum obstruction

Outputs are located in:

results/object_tests/
results/analysis/object_comparison/
Indoor Distance Tests

Indoor distance testing evaluated how channel metrics changed with receiver separation.

Distances:

6 ft
10 ft
15 ft

Outputs are located in:

results/distance_tests/
results/analysis/distance_comparison/
Outdoor Tests

Outdoor testing compared indoor propagation to outdoor line-of-sight and obstructed environments.

Scenarios:

Outdoor LOS
Outdoor obstructed

Outputs are located in:

results/outdoor_tests/
results/analysis/indoor_outdoor_comparison/
Key Results

Major observations:

Indoor channels showed strong multipath behavior due to reflections from walls, objects, and room geometry.
Object obstruction tests showed measurable changes in peak-to-mean ratio, mean correlation floor, and CIR structure.
Indoor distance tests showed spatial sensitivity, where small position changes altered channel metrics.
Outdoor LOS measurements produced lower RMS delay spread than indoor measurements.
Outdoor obstructed testing reintroduced scattering and increased delay spread relative to outdoor LOS.
Smoothed CIR overlays showed visibly different channel structures across indoor, outdoor LOS, and outdoor obstructed environments.
Example Final Analysis Outputs

Important final figures include:

results/analysis/final_overlays/final_environment_overlay_smoothed.png
results/analysis/indoor_outdoor_comparison/indoor_outdoor_rms_spread.png
results/analysis/object_comparison/object_peak_ratio.png
results/analysis/distance_comparison/distance_peak_ratio.png
results/analysis/bandwidth_comparison_v7/fwhm_vs_bandwidth.png
How to Run

Install dependencies:

pip install -r requirements.txt

Generate PN sequence:

python3 scripts/sdr_capture/make_pn_v2.py

Transmit PN waveform:

sudo python3 scripts/sdr_capture/tx_pn_v3_highpower.py

Process received capture:

python3 scripts/signal_processing/plot_cir_v6b_export_csv.py

Run final comparison overlays:

python3 scripts/analysis/final_overlay_v1.py
Capstone Summary

This project demonstrates a functioning SDR-based wireless channel sounding platform. The system successfully measures real-world wireless propagation behavior and supports controlled experiments for analyzing multipath, obstruction, distance, and environmental effects.
