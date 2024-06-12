# SPICE-Based SNN Simulator

[![Documentation Status](https://readthedocs.org/projects/snn_simulator/badge/?version=latest)](https://salah-daddi-nounou.github.io/)

## Overview

This project provides a framework for simulating spiking neural networks (SNNs) with spintronic synapses at the SPICE level. The framework automates the design, simulation, and analysis of SNNs, integrating various tools and scripts to streamline the process.

## Features

- **Automatic Netlist Generation**: Generate netlists for SNNs of any size based on user-defined parameters.
- **SPICE Simulation**: Automate SPICE simulations using the Cadence Spectre simulator.
- **Parallel Processing**: Run multiple simulations in parallel to explore different network configurations.
- **Result Analysis**: Plot the history of synaptic weights and membrane potentials, and calculate Euclidean distances to evaluate training quality.

## Documentation

Comprehensive documentation for the framework, including setup instructions, usage guides, and API references, is available at the following link:

[![Documentation](https://img.shields.io/badge/documentation-available-blue)](https://salah-daddi-nounou.github.io/)

## Getting Started

### Prerequisites

Ensure you have the following software installed:

- Python 3.x
- Cadence Spectre simulator
- Required Python libraries: numpy, matplotlib, argparse

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/salah-daddi-nounou/snn_simulator.git
cd snn_simulator
```

If you use this framework, please cite our publication:

```
bibtex
Copy code
@article{daddinounou2024spice,
  title={SPICE-Level Demonstration of Unsupervised Learning with Spintronic Synapses in Spiking Neural Networks},
  author={Daddinounou, Salah and Gebregiorgis, Anteneh and Hamdioui, Said and Vatajelu, Elena-Ioana},
  journal={IEEE Access},
  year={2024},
  publisher={IEEE}
}
```