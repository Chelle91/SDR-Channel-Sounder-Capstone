# Scripts Directory

This directory contains all SDR capture, signal-processing, and analysis scripts used throughout the project.

## Directory Structure

### `sdr_capture/`
Scripts responsible for waveform generation, SDR transmission, and IQ capture.

### `signal_processing/`
Scripts responsible for CIR extraction, coherence bandwidth estimation, PDP generation, and intermediate processing operations.

### `analysis/`
Higher-level analysis and visualization scripts used to generate overlays, comparative figures, FFT-based heatmaps, and publication-ready plots.

## Development Philosophy

The processing pipeline was intentionally modular to support:

- Repeatable experimentation
- Offline debugging
- Reproducible analysis
- Rapid visualization development
