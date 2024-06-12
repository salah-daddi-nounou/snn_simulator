<div align='center'>
<h1>SPICE-Based SNN Simulator</h1>
</div>

[![Documentation Status](https://readthedocs.org/projects/snn_simulator/badge/?version=latest)](https://salah-daddi-nounou.github.io/snn_simulator/)

## Overview

This project provides a framework for simulating spiking neural networks (SNNs) with spintronic synapses at the SPICE level. The framework automates the design, simulation, and analysis of SNNs, integrating various tools and scripts to streamline the process.

## Features

- **Automatic Netlist Generation**: Generate netlists for SNNs of any size based on user-defined parameters.
- **SPICE Simulation**: Automate SPICE simulations using the Cadence Spectre simulator.
- **Parallel Processing**: Run multiple simulations in parallel to explore different network configurations.
- **Result Analysis**: Plot the synaptic history and membrane potentials, and evaluate training quality under variability.

## Documentation

Usage guide and comprehensive documentation are available [here](https://salah-daddi-nounou.github.io/snn_simulator/)

## Getting Started

### Prerequisites

Ensure you have the following software installed:

- Python 3.x
- Cadence Spectre simulator licence
- Required Python libraries: numpy & matplotlib

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/salah-daddi-nounou/snn_simulator.git
cd snn_simulator
```

If you use this framework, please cite our publication:

```
@article{daddinounou2024spice,
  title={SPICE-Level Demonstration of Unsupervised Learning with Spintronic Synapses in Spiking Neural Networks},
  author={Daddinounou, Salah and Gebregiorgis, Anteneh and Hamdioui, Said and Vatajelu, Elena-Ioana},
  journal={IEEE Access},
  year={2024},
  publisher={IEEE}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
