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
variables = {'sim_time' : 150e-3, 'spike_duration' : 10e-3, 'mem_vth': 12e-3,           
             'num_input': 25, 'num_output': 1, 'num_cells': 2,
             'cod_base' : 3, 'cod_max' : 10, 'inp_img': 'X', 'dev': 0}

# Preapare combinations to run multiprocessing simulations
param_combinations = []
#inp_img = ['I','O','C','F','H','K','L','P','T','U']
#deviation = [i/100 for i in range(0,25,5)]
deviation = [0]
mtjs = [2] 

for a in deviation:
  for b in mtjs:
    variables['dev'] =a
    variables['num_cells'] = b
    param_combinations.append(variables.copy())

def run_simulation(params):
    '''
    run_simulation takes an initial dict containing global parameters
    and adds other local parameters to that dict 
    '''
    #Load and flatten spiking neurons intensity
    input_data = np.load(f'./input_images/letter_imgs/generated_{params["inp_img"]}.npy')
    flat_input_data = input_data.flatten()
    # We use frequency coding proportional to pixel intensity + baseline
    n_spik_vec = params['cod_base'] + params['cod_max'] *(flat_input_data/255.0)    
    params['num_input'] = len(flat_input_data)

    # create a string that contians result signals, to insert in .ocn file 
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
    # Format date and time as a string in the format 'MMDD_HHMM'
    now = datetime.datetime.now()
    date = now.strftime("%m%d_%H%M")     
    process_dir = f"dat_{date}_pross_{os.getpid()}"          # name the folder with date,time & process
    abs_process_dir = os.path.join(base_dir, process_dir)
    
    # Creat a proces-specific directory for simulation files and results
    if not os.path.exists(abs_process_dir):   
        os.mkdir(abs_process_dir)             
        os.mkdir(abs_process_dir+"/netlist_ocn")
    copy_tree("./netlist_ocn", f"{abs_process_dir}/netlist_ocn")   
    netlist = os.path.join(abs_process_dir,"netlist_ocn","netlist")
    results_file = os.path.join(abs_process_dir, "results.txt") 

    # params to include in .ocn file
    params["netlist"] = netlist                              # path to the complete netlist file 
    params["process_dir"] = abs_process_dir                  # pathe to simulation process dir
    params["results_file"] = results_file                    # path to the file where results are written 
    params["save_states"] = save_states                      # a string contains signals to be written in results file
   
    network_generator = NetworkGenerator(netlist, params['num_input'], params['num_output'], params['num_cells'], n_spik_vec)
    network_generator.generate_netlist_file()                # the comlete netlist file is created 
        
    updated_template_file = os.path.join(abs_process_dir, f"updated_template.ocn")
    log_file = os.path.join(abs_process_dir, f"oceanScript.log") 
    subst_run.substitute_templ("./mp_oceanScript.ocn", updated_template_file, params)
    subst_run.exec_cmd(f"ocean -nograph < {updated_template_file} > {log_file}") 

def main():
    with Pool() as p:
        p.map(run_simulation, param_combinations)            # distribute combinations sets and run
        simul_t = datetime.timedelta(seconds=tm.time()-start_time)
    print(f" --- The simulation finished after {simul_t} - at {datetime.datetime.now()} ---")

if __name__ == '__main__':
    main()

