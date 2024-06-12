# Usage 
A guide to using the SNN Simulator framework is provided here. It covers setting up the SNN design and simulation parameters, launching the simulations, and plotting the results. For the requirements, you only need `Candence Spectre` licence instaled, along with `python3` with `numpy` and `matplotlib` packages. As of the current development of the project, no specific PDK is required.  

## Setting Up Simulations

### Step 1: Configuring the design & Simulation Parameters

The SNN design and simulation parameters are configured in the `snn_simulator.py` script. Here, you can specify the number of input and output neurons, the number of MTJs per synapse, the spike duration, and other simulation-specific parameters.

Example configuration in `snn_simulator.py`:

```python
# Chosen design parameters
variables = {
    'sim_time': 150e-3,
    'spike_duration': 10e-3,
    'mem_vth': 12e-3,
    'num_input': 25,
    'num_output': 1,
    'num_cells': 2,
    'cod_base': 3,
    'cod_max': 10,
    'inp_img': 'U',
    'dev': 0
}

# Prepare combinations to run multiprocessing simulations
param_combinations = []

inputs = ['I', 'O', 'C', 'F', 'H', 'K', 'L', 'P', 'T', 'U', 'X']
deviation = [i / 100 for i in range(0, 25, 5)]
mtjs = [2, 4, 6, 8]

for a in inputs:
    for b in deviation:
        for c in mtjs:
            variables['inp_img'] = a
            variables['dev'] = b
            variables['num_cells'] = c
            param_combinations.append(variables.copy())
```

In this example, we create combinations of different inputs, number of MTJs composing a synapse, and diffrent standard deviations for variability distributions in the synapses. Each combination of these parameters represents a unique SNN design that will be simulated in parallel. In this case, `param_combinations` will have a length of 220, corresponding to the number of SNN that will simulated simultanuously. 

### Step 2: Running the Simulation
Run the `snn_simulator.py` script from `snn_simulator/src/` directory to start the simulations. We recommand creating a separate directory for the simulation results outside of the project, like `../../snn_sim_folders`. The framework will automatically create different folders in that directory for each simulation configuration. Each folder will contain the generated netlist, the updated `.ocn` script, and a `results.txt` file with the simulation results.

```bash
>> python snn_simulator.py
```
Each run of `python snn_simulator.py` will execute the created SNN design simulations in parallel. The only limitation of the number of concurrent simulations will be the available number of CPU threads. If the number of simulations exceeds the available threads, the additional simulations will queue and start as soon as a CPU thread becomes available.

## Structure of Simulation Result Folders

Each simulation generates SNN folders in the `../../snn_sim_folders` directory with a specific naming convention. The folder names are automatically generated to include the date and time when the simulation was started, process ID of the simulation run, followed by the explored parameters in that simulation, in our previous example that owuld be : tletter (input image), variability std, and the number of MTJs (cells). The general format for naming the simulation result folders is:

`dat_<date>_<time>_pross<process_id>_param1<param1value>_param2<param2value>.../`

*Example:* 

```
dat_1225_1719_pross_48757_letX_dev0.15_cells8
dat_1225_1721_pross_48748_letX_dev0.15_cells2
dat_1225_1721_pross_48760_letX_dev0.0_cells2
```

Each of these simulation folders corresponds to a certain SNN design and contains the `netlist` files, `updated_template.ocn` script, and `results.txt` file containing the history of the weights of synapses and the output neuron membrane potential.

```
dat_1225_1719_pross_48757_letX_dev0.15_cells8/
├── netlist
├── netlist_ocn
│   ├── input.scs
│   ├── netlist
│   ├── netlistFooter
│   ├── netlistHeader
├── results.txt
└── updated_template.ocn
```

## Plotting the Results

### Plotting Weight and Membrane Potential

The `plot_weig_membr.py` script reads the simulation results from the `results.txt` file in a specified folder. It then plots the history of the synaptic weights and the membrane potential of the output neuron over the course of the simulation. It also displays a reconstructed image of the synapses states before and after training.  

#### Usage

```bash
python plot_weig_membr.py <simulation_folder>
```

### Plotting Euclidean Distance

The `plot_eucl_dist.py` script evaluates the training quality of the synapses by calculating and plotting the Euclidean distance between the input pattern and the synapse conductance pattern after training. This metric is used because the small network is trained on one pattern at a time, making accuracy measures less relevant. By comparing the states of the synapses after training under various variability conditions, the script visualizes the impact of variability on synaptic learning. This analysis can be extended to different SNN configurations using different numbers of MTJs per synapse.

#### Usage

```bash
python plot_eucl_dist.py
```
