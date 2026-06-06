# Results Directory

This directory contains all experimental datasets, extracted metrics, generated figures, and comparative propagation analysis results for the SDR-based wireless channel sounder project.

## Directory Structure

### `distance_tests/`
Indoor line-of-sight distance sweep experiments comparing propagation behavior across multiple transmitter-to-receiver separations.

### `object_tests/`
Obstruction experiments evaluating how materials such as cardboard, wood, aluminum, and human blockage affect multipath propagation and correlation structure.

### `outdoor_tests/`
Outdoor line-of-sight and obstructed propagation experiments used to compare environmental propagation behavior against indoor measurements.

### `bandwidth_tests/`
Bandwidth-dependent experiments analyzing temporal resolution and CIR sharpness across multiple SDR bandwidth configurations.

### `analysis/`
Processed overlays, comparative plots, FFT-based visualizations, coherence bandwidth analysis, and aggregate experimental figures.

### `coherence_v7/`
Coherence bandwidth calculations and visualization outputs derived from FFT-based frequency-domain analysis.

## Metrics

Experimental analysis included:

- RMS delay spread
- Peak-to-mean ratio
- Mean correlation floor
- CIR comparative structure
- Bandwidth-dependent peak width analysis
- Frequency-selective fading behavior
