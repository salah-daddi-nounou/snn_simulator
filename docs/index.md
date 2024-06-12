<h1 style="text-align: center;">SNN Training Framework</h1>

## Introduction

The SNN Training Framework streamlines the design, training, and analysis of Spiking Neural Networks (SNNs) with electrical simulations. These simulations aim to validate the concept of hardware implementation of SNNs with spintronic synapsees, which are energy effecient and allow unsupervised learning. The tool automates the generation of netlists for SPICE, running simulations with `Cadence Spectre`, and analyzing the results. It facilitates efficient exploration of various SNN configurations with a high degree of customization, with miminum intervintion from the user.

## Features

- **Automated Netlist Generation**: Automatically generates detailed netlists essential for accurately modeling SNN behavior at the device level, using customizable parameters.
- **Integration with SPICE Simulator**: Seamlessly integrates with `Cadence Ocean` tool and uses `Spectre` simulator, allowing electrical simulation, without much worrying about the design and resutls handelign. 
- **Parallel Processing Capabilities**: Supports multiprocessing to conduct parallel simulations and parametric analysis, crucial for simultaneous and fast design exploration of different SNNs. 
- **Performance Analysis**: Provides comprehensive post-simulation results, including synaptic weight evolution, neuron membrane potential dynamics, and overall learning performance, with minimal user input beyond the initial setup.

## Project Background

Simulation environments for SNNs vary widely based on their objectives, from functional to behavioral simulations. Electrical simulations with SPICE are critical for hardware implementation as they model synaptic conductance and neuron membrane potentials using actual voltages and currents, providing essential validation for hardware implementations. This project was initially concieved during a PhD to automate design explorations that simulate training of SNNs with MTJ-based synapses, with a specific learing rule, but can be adapted for other type of synapses and learning rules. Conducting SNN training in SPICE validates learning rules like STDP and demonstrates the feasibility of online learning through dynamic conductance changes in spintronic synapses. Although SPICE simulations are computationally expensive, they offer rigorous, hardware-accurate results suitable for small networks.

Development and training of SNNs at the device level pose some challenges, especially in network design, which often involves creating complex schematics or manually writing netlists. This process is time-consuming and prone to errors. This framework addresses these challenges by automating the design and training of SNNs with electrical simulations. By automating these processes, we save time and reduce the potential for human error, making it significantly easier to manage and explore various network configurations efficiently.


## Overview
The tool handles the design and netlist creation, while the actual simulations are executed in SPICE. The design consists of input and output neurons described in Verilog-A, fully conencted by spintornic synapses. Each synapse is composed of multiple Magnetic Tunnel Junction (MTJs) connected in parallel. The learning rule is derived from the physical behaviour of the stochastic synapse and is labeled Bi-Sigmoid STDP. 


### Device Models

The framework includes the following Verilog-A device description models:

1. **MTJ Model**: Integrates the electrical and magnetic behavior of the MTJ and simulates its use as a two-state memory device. 
2. **Input Neuron Model**: A spiking neuron model that encodes the input images and feed them to the network.
3. **Output Neuron Model**: A leaky integrate-and-fire neuron model used as an output neuron.

### Netlist Generation

Along with these necessary device descriptions, a netlist that describes the full network is required. The framework allows automatic generation of a netlist for SNNs of any size. The operator only needs to input basic information such as the number of input and output neurons, the number of MTJs per synapse, and a time window during which an input image is presented to the network. The framework then generates the corresponding netlist.

### Simulation and Analysis

Once the netlist has been generated, the simulation is launched automatically in `Spectre`. It inputs the image pixels to the network, the input neurons spike according to a given coding, and the signal is fed forward in the form of current, allowing the network to learn the patterns using the B2STDP rule, which is specific to SNNs. The framework tracks the history of each synapse and neuron in the network and provides different plotting and visualization functionalities.
