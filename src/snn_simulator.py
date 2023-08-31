import run_main 
import time as tm
import datetime
import numpy as np
from multiprocessing import Pool
import os
from distutils.dir_util import copy_tree
from net_generator import *

start_time = tm.time()
# chosen design paraeters
variables = {'n_mtj': 4,'W_pre': 60e-3, 'V_pre': 150e-3, 'V_pre_end':-90e-3, 'W_post_max': 1e-6, 'W_post_min': 7e-6, 'V_post_max': 100e-3, 'V_post_min': -100e-3}  
MC=1    # number of statistical Monte Carlo simulations to be run  

# Preapare combinations to run multiprocessing simulations
param_combinations = []
param_combinations.append(variables.copy())

# SNN caracteristics
num_input = 25
num_output = 1
num_cells = 6

sim_time = 1e-3#600e-3                                   # (s) duration of simulation & input presentaion
spike_duration = 60e-3                              # (s) duration of input spikes
mem_vth = 50e-3                                     # (V) output membrane potential threshold 

# input coding : n_spikes = base + max (pixel/255)
cod_base = 3; cod_max = 2

# create a string that contians result signals, to inserct in .ocn file 
save_states = "" 
for i in range(1, num_input*num_output + 1):
    input_index = (i - 1) % num_input + 1
    output_index = (i - 1) // num_input + 1
    for j in range(1, num_cells+1):
        save_states +='v("synapse{}_{}.cell{}.I:ix") '.format(input_index, output_index,j)
# If you want to print the history of eahch MTJ, remove the follwing 2 lines
        if j < num_cells:
            save_states += '+'

def run_simulation(params):
    '''
    run_simulation takes an initial dict containing global parameters
    and adds other local parameters to that dict 
    '''
    tic = tm.time()   

    base_dir = os.path.abspath("../../snn_sim_folders/")
    process_dir = f"process_{os.getpid()}"
    abs_process_dir = os.path.join(base_dir, process_dir)

    if not os.path.exists(abs_process_dir):   
        os.mkdir(abs_process_dir)             
        os.mkdir(abs_process_dir+"/netlist_ocn")
    copy_tree("./netlist_ocn", f"{abs_process_dir}/netlist_ocn")   
    netlist = os.path.join(abs_process_dir,"netlist_ocn","netlist")
    results_file = os.path.join(abs_process_dir, "results.txt") 

    # params to include in .ocn file
    params["netlist"] = netlist                      # path to the complete netlist file 
    params["process_dir"] = abs_process_dir          # pathe to simulation process dir
    params["results_file"] = results_file            # path to the file where results are written 
    params["save_states"] = save_states              # a string contains signals to be written in results file
    params["sim_time"] = sim_time                    # total simulation time (currently: duration during which an input is presented) 
    params["spike_duration"] = spike_duration         # input spike duration 
    params["mem_vth"] = mem_vth                      # output membrane potential threshold  
   
    #Load and flatten spiking neurons intensity
    input_data = np.load('input_data.npy')
    flat_input_data = input_data.flatten()
    n_spik_vec = cod_base + cod_max *(flat_input_data/255.0)   # normlize and add baseline for frequency coding 

    for i in range(MC):
        
        network_generator = NetworkGenerator(netlist, num_input, num_output, num_cells, n_spik_vec)
        network_generator.generate_netlist_file()    # the comlete netlist file is created 
        
        updated_template_file = os.path.join(abs_process_dir, f"updated_template.ocn")
        log_file = os.path.join(abs_process_dir, f"oceanScript.log") 
        run_main.subs_template_file("./mp_oceanScript.ocn", updated_template_file, params)
        run_main.run_command(f"ocean -nograph < {updated_template_file} > {log_file}") 

'''
        data = np.genfromtxt(results_file, delimiter="", skip_header=4)
#        if len(data) == 35:    #length of the delay2 list
        if i == 0:
            avg_data = data
        else:
            avg_data = (avg_data + data) / 2        
#        else:
#            print(f"skipped : data length not compatible in iteration {i}")

    with open( abs_process_dir+'/sliced_array.txt', 'a') as outfile:
        result  = np.hstack(( np.array(len(avg_data) * [list(params.values())[:8]]) , avg_data ))
        outfile.write(f"#{str(list(params.items())[:8])}\n")
        np.savetxt(outfile, result, fmt='%.3e')
        prss_t = datetime.timedelta(seconds=tm.time()-tic)
        outfile.write(f"\n # --- The {abs_process_dir} finished after {prss_t} - at {datetime.datetime.now()} ---\n")
'''

def main():
    with Pool() as p:
        p.map(run_simulation, param_combinations)   # distribute combinations sets and run
        simul_t = datetime.timedelta(seconds=tm.time()-start_time)
    print(f" --- The simulation finished after {simul_t} - at {datetime.datetime.now()} ---")

if __name__ == '__main__':
    main()

