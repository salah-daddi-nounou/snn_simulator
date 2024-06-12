"""
This is the main module that orchestrates the simulation process of SNN. It
handles the creation of input images, netlist generation, parameter substitution, 
and execution of the simulation, along with the collection of results.

This module:
    1. Accepts user-specificatied parameter combinations for different SNN designs.
    2. Loads the generated input images, flattens them, and uses frequency coding proportional to pixel intensity
    3. Generates files and process-specific directory for each SNN simulation named with the date, process ID, and parameter details 
    4. Creates the netlist for each simulation using the net_generator module.
    5. Substitutes parameters into the OCEAN script template and launches the SPICE simulation using the subst_run module. 
    6. Collects and saves the waveforms results of the selected signals.
    7. Executes the simulations of different SNN designs in parallel. 
"""

import subst_run 
import time as tm
import datetime
import numpy as np
from multiprocessing import Pool
import os
from distutils.dir_util import copy_tree
from net_generator import *
import shutil

'''
Input images are stored in binary formats (individually: .npy arrays, 
and collectively: .pkl dict) all files generated at once. 
'''
start_time = tm.time()

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

inputs = ['I','O','C','F','H','K','L','P','T','U','X']
deviation = [i/100 for i in range(0, 25, 5)]
mtjs = [2, 4, 6, 8] 

for a in inputs: 
    for b in deviation:
        for c in mtjs:
            variables['inp_img'] = a  
            variables['dev'] = b
            variables['num_cells'] = c
            param_combinations.append(variables.copy())

def run_simulation(params):
    """
    Runs a single SNN simulation with the given parameters.

    Args:
        params (dict): A dictionary containing global and local simulation parameters.

    Steps:
        1. Load and flatten input image.
        2. Calculate the number of spikes for each input neuron based on pixel intensity.
        3. Generate and prepare directories and files for the simulation.
        4. Create the netlist for the simulation.
        5. Substitute parameters into the OCEAN script and run the simulation.
        6. Clean up temporary files.
    """
    # Load and flatten spiking neurons intensity
    input_data = np.load(f'./input_images/letter_imgs/generated_{params["inp_img"]}.npy')
    flat_input_data = input_data.flatten()
    # Use frequency coding proportional to pixel intensity + baseline
    n_spik_vec = params['cod_base'] + params['cod_max'] * (flat_input_data / 255.0)    
    params['num_input'] = len(flat_input_data)

    # Create a string that contains result signals, to insert in .ocn file 
    save_states = "" 
    for i in range(1, params['num_input'] * params['num_output'] + 1):
        input_index = (i - 1) % params['num_input'] + 1
        output_index = (i - 1) // params['num_input'] + 1
        for j in range(1, params['num_cells'] + 1):
            save_states += f'v("synapse{input_index}_{output_index}.cell{j}.I:ix") '
            if j < params['num_cells']:
                save_states += '+'

    base_dir = os.path.abspath("../../snn_sim_folders/")
    # Format date and time as a string in the format 'MMDD_HHMM'
    now = datetime.datetime.now()
    date = now.strftime("%m%d_%H%M")     
    #process_dir = f"dat_{date}_pross_{os.getpid()}"          # name the folder with date,time & process
    process_dir = f"dat_{date}_pross_{os.getpid()}_let{params['inp_img']}_dev{params['dev']}_cells{params['num_cells']}" #include the paramters with date & process

    abs_process_dir = os.path.join(base_dir, process_dir)
    
    # Create a process-specific directory for simulation files and results
    if not os.path.exists(abs_process_dir):   
        os.mkdir(abs_process_dir)             
        os.mkdir(abs_process_dir + "/netlist_ocn")
    copy_tree("./netlist_ocn", f"{abs_process_dir}/netlist_ocn")   
    netlist = os.path.join(abs_process_dir, "netlist_ocn", "netlist")
    results_file = os.path.join(abs_process_dir, "results.txt") 

    # Params to include in .ocn file
    params["netlist"] = netlist  # Path to the complete netlist file 
    params["process_dir"] = abs_process_dir  # Path to simulation process dir
    params["results_file"] = results_file  # Path to the file where results are written 
    params["save_states"] = save_states  # A string containing signals to be written in results file
   
    random.seed(10)
    network_generator = NetworkGenerator(netlist, params['num_input'], params['num_output'], params['num_cells'], n_spik_vec)
    network_generator.generate_netlist_file()  # The complete netlist file is created 
        
    updated_template_file = os.path.join(abs_process_dir, "updated_template.ocn")
    log_file = os.path.join(abs_process_dir, "oceanScript.log") 
    subst_run.substitute_templ("./oceanScript.ocn", updated_template_file, params)
    subst_run.exec_cmd(f"ocean -nograph < {updated_template_file} > {log_file}") 
    shutil.rmtree(f"{abs_process_dir}/psf")  # Remove the psf directory

def main():
    """
    Main function to run all simulations using multiprocessing.
    
    Steps:
        1. Distribute parameter combinations across multiple processes.
        2. Run simulations in parallel.
        3. Measure and print the total simulation time.
    """
    with Pool() as p:
        p.map(run_simulation, param_combinations)  # Distribute combinations sets and run
        simul_t = datetime.timedelta(seconds=tm.time() - start_time)
    print(f" --- The simulation finished after {simul_t} - at {datetime.datetime.now()} ---")

if __name__ == '__main__':
    main()
