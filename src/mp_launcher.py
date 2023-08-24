import run_main 
import time as tm
import numpy as np
from multiprocessing import Pool
import os
from distutils.dir_util import copy_tree

start_time = tm.time()
seeds_def = run_main.parse_params_file("./parameter.txt")  

variables = {'W_pre': 40e-3, 'V_pre': 150e-3, 'V_pre_end':-90e-3, 'W_post_max': 1e-6, 'W_post_min': 7e-6, 'V_post_max': 100e-3, 'V_post_min': -100e-3}  
MC=1

W_pre     = [1e-3*x for x in [60]]
V_pre_end = [1e-3*x for x in [-90]]
W_post_min    = [1e-6*x for x in [7]]
V_post    = [1e-3*x for x in [100]]

total_iter = MC * len(W_pre) * len(V_pre_end) * len(W_post_min) * len(V_post)
param_combinations = []

for a in W_pre:
    for b in V_pre_end:
        for c in W_post_min:
            for d in V_post:
                variables['W_pre'] =a
                variables['V_pre_end'] =b
                #variables['W_post_max'] =c
                variables['W_post_min'] =c
                variables['V_post_max'] =d
                variables['V_post_min'] =-d
                param_combinations.append(variables.copy())

def run_simulation(params):
    
    process_dir = f"process_{os.getpid()}"                                                                     
    abs_process_dir = os.path.abspath(process_dir) 
    if not os.path.exists(process_dir):   
        os.mkdir(process_dir)             
        os.mkdir(process_dir+"/netlist_ocn")
    copy_tree("./netlist_ocn", f"./{process_dir}/netlist_ocn")   
    #copy_tree("./netlist_ocn", f"./{process_dir}/netlist_ocn")   
    netlist = os.path.join(abs_process_dir,"netlist_ocn","netlist")
    results_file = os.path.join(process_dir, "results.txt") 

    params["netlist"] = netlist
    params["process_dir"] = abs_process_dir  
    params["results_file"] = results_file  
    for i in range(MC):
        seeds = run_main.generate_params(seeds_def)
        all_params = {**seeds, **params}
        updated_template_file = os.path.join(process_dir, f"updated_template.ocn")
        log_file = os.path.join(process_dir, f"oceanScript.log") 
        run_main.subs_template_file("./bc_oceanScript.ocn", updated_template_file, all_params)
        run_main.run_command(f"ocean -nograph < {updated_template_file} > {log_file}") 

        data = np.genfromtxt(results_file, delimiter="", skip_header=4)
#        if len(data) == 35:    #length of the delay2 list
        if i == 0:
            avg_data = data
        else:
            avg_data = (avg_data + data) / 2        
#        else:
#            print(f"skipped : data length not compatible in iteration {i}")

    with open( process_dir+'/sliced_array.txt', 'a') as outfile:
        result  = np.hstack(( np.array(len(avg_data) * [list(params.values())[:7]]) , avg_data ))
        outfile.write(f"#{str(list(params.items())[:7])}\n")
        np.savetxt(outfile, result, fmt='%.3e')

def main():
    with Pool() as p:
        p.map(run_simulation, param_combinations)

    t_sim = tm.time() - start_time
    print("--- process finished in: %s seconds ---" % t_sim)

if __name__ == '__main__':
    main()

