# Scenario Comparison Analysis

This directory contains comparative metrics and visualization outputs from the initial SDR channel sounding validation experiments conducted during early system development.

These experiments were used to:
- validate PN-sequence channel sounding operation
- evaluate repeatability of the SDR capture pipeline
- compare LOS and NLOS propagation behavior
- establish baseline multipath performance metrics

## Included Scenarios

### Baseline LOS
Initial short-range indoor line-of-sight reference measurement used to verify system functionality and establish baseline propagation characteristics.

### LOS 3 ft
Indoor line-of-sight measurement conducted at approximately 3 ft separation between transmitter and receiver.

### LOS 5.25 ft
Indoor line-of-sight measurement conducted at approximately 5.25 ft separation to evaluate distance-related propagation behavior and delay spread changes.

### NLOS Obstructed
Indoor non-line-of-sight measurement with physical obstruction introduced between transmitter and receiver to evaluate attenuation and multipath effects.

### Repeatability
Repeated measurement scenario used to evaluate consistency and stability of the SDR capture and processing pipeline across multiple acquisitions.

## Metrics

The plots and exported metrics summarize:
- RMS delay spread
- Mean delay
- Peak-to-mean correlation ratio
- Correlation floor behavior

These early-stage experiments informed the later refined indoor/outdoor and bandwidth-focused propagation studies included elsewhere in the repository.
