import subst_run 
import time as tm
import datetime
import numpy as np
from multiprocessing import Pool
import os
from distutils.dir_util import copy_tree
from net_generator import *

start_time = tm.time()
# chosen design paraeters
variables = {'n_mtj': 4,'W_pre': 60e-3, 'V_pre': 150e-3, 'V_pre_end':-90e-3, 'W_post_max': 1e-6, 'W_post_min': 7e-6, 'V_post_max': 100e-3, 'V_post_min': -100e-3,
             'sim_time' : 10e-6, 'spike_duration' : 10e-3, 'mem_vth': 10e-3,           
             'num_input': 25, 'num_output': 1, 'num_cells': 2,
             'cod_base' : 3, 'cod_max' : 4}

# Preapare combinations to run multiprocessing simulations
param_combinations = []
num_output = [1,2,3]
for a in num_output:
    variables['num_output'] =a
    param_combinations.append(variables.copy())

def run_simulation(params):
    '''
    run_simulation takes an initial dict containing global parameters
    and adds other local parameters to that dict 
    '''
    tic = tm.time()   

    # create a string that contians result signals, to inserct in .ocn file 
    save_states = "" 
    for i in range(1, params['num_input']*params['num_output'] + 1):
        input_index = (i - 1) % params['num_input'] + 1
        output_index = (i - 1) // params['num_input'] + 1
        for j in range(1, params['num_cells']+1):
            save_states +='v("synapse{}_{}.cell{}.I:ix") '.format(input_index, output_index,j)
    # If you want to print the history of eahch MTJ, remove the follwing 2 lines
            if j < params['num_cells']:
                save_states += '+'

    base_dir = os.path.abspath("../../snn_sim_folders/")
    
    # Get current date and time
    now = datetime.datetime.now()
    # Format date and time as a string in the format 'MMDD_HHMM'
    date = now.strftime("%m%d_%H%M")     
    process_dir = f"dat_{date}_pross_{os.getpid()}"             # name the folder with date,time & process
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
   
    #Load and flatten spiking neurons intensity
    input_data = np.load('./input_images/generated_npy/generated_1.npy')
    flat_input_data = input_data.flatten()
    # input coding : n_spikes = base + max *(pixel/255)
    n_spik_vec = params['cod_base'] + params['cod_max'] *(flat_input_data/255.0)   # normlize and add baseline for frequency coding 
    
    network_generator = NetworkGenerator(netlist, params['num_input'], params['num_output'], params['num_cells'], n_spik_vec)
    network_generator.generate_netlist_file()    # the comlete netlist file is created 
        
    updated_template_file = os.path.join(abs_process_dir, f"updated_template.ocn")
    log_file = os.path.join(abs_process_dir, f"oceanScript.log") 
    subst_run.substitute_templ("./mp_oceanScript.ocn", updated_template_file, params)
    subst_run.exec_cmd(f"ocean -nograph < {updated_template_file} > {log_file}") 

def main():
    with Pool() as p:
        p.map(run_simulation, param_combinations)   # distribute combinations sets and run
        simul_t = datetime.timedelta(seconds=tm.time()-start_time)
    print(f" --- The simulation finished after {simul_t} - at {datetime.datetime.now()} ---")

if __name__ == '__main__':
    main()

