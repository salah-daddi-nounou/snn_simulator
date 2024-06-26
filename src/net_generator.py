'''
Spice simulation with Spectre simulator requires a netlist file that includes the description of all the components of the circuit, and describes how these componenents are wired. The framework allows flexible geneartion of the netlist according to the desired network to be simulated. Only some network parameters should be given, for the corresponding netlist to be automatically generated.  The follwoing module `net_generator.py` which contains diffrent classes is responsible of generating the netlist.
Circuit componenents are mangaged by the follwing classes : `Synapse`, `Synapse_subskt`, `Input_neuron`, `Output_neuron`, each contains a `generate_netlist_bloc` method that sets a string template bloc specific to that componenent and which should be added to the netlist file.
The class `Netlist` concatinates the instances of the componenets in a list, and generates a string bloc of a single componenent ready to be inserted in the final netlist.
The class `NetworkGenerator` is the main class that assembles all the components by iterating the appending method of `Netlist` class. and trigers the netlist generation method of `Netlist`.
Finally `Separotor` is a class to add a separation between a group of similar componenets for a bette rformatting.
'''

import random
class Synapse:
    """
    A class to specify a netlist bloc that describes an MTJ-based synapse of the SNN, 
    generate_netlist_bloc is a method that returns as string which represents a template 
    bloc of the synapse to be included in the netlist later. It personalizes the synapse
    at the current iteration by adding its specific informatio (connected neurons, number 
    of MTJs per synapse, initialized states, seeds,... ). The synapse template calls the 
    compound_synapse subcircuit which should be included once in the head of the netlist.

    Attributes:
        input_index [int]: The index of the input neuron connected to this synapse.
        output_index [int]: The index of the output neuron connected to this synapse.
        paps [list of int]: The list of initial states of free layers for each MTJ in the synapse. (0 parallel, 1 anti-parallel).
        seeds [list of int]: The list of seed values used for stochasticity for each MTJ in the synapse.

    Methods
    -------
    generate_netlist_bloc():
        Generates a string bloc specefic to that synapse in the final netlist file. 

    """

    def __init__(self, input_index, output_index, num_cells):
        self.input_index = input_index
        self.output_index = output_index
        self.seeds = [random.randint(0, 9999) for _ in range(num_cells)]
        #self.paps = [i%2 for i in range(num_cells)]                 # alternate 0&1 in the MTJs of the synapse
        self.paps = [random.randint(0, 1) for _ in range(num_cells)] #initialize randamely

    def generate_netlist_bloc(self):                 
        template = "synapse{}_{} (input{} output{}) compound_synapse "
        paps_str = " ".join("PAP{}={}".format(i + 1, pap) for i, pap in enumerate(self.paps))
        seeds_str = " ".join("seed{}={}".format(i + 1, seed) for i, seed in enumerate(self.seeds))
        return template.format(
            self.input_index, self.output_index, self.input_index, self.output_index
        ) + paps_str + " \\\n\t\t" + seeds_str + "\n"

class Synapse_subskt:
    """
    A class to specify a netlist bloc of the synapse subcircuit named compound_synapse, 
    which will be called by all the synapses. It is composed of multiple MTJs (the number is given as attribute), 
    and it makes call of the cellPMAMTJ subcircuit which is predefined in the initial netlist file.
    generate_netlist_bloc is a method that returns the subcircuit template to be included in the netlist.
    It takes an initial template, adds parameters to it : either to set stochasticity, variability,
    temperature and its variation or not, and sets as parameters the initial state of the MTJ, and the seed. 

    Attributes:
        num_cells [int]: The number of MTJ cells in each synapse.


    Methods
    -------
    generate_netlist_bloc():
        Generates a string bloc specefic to the compound_synapse subcircuit in the final netlist file. 
    """

    def __init__(self, num_cells):
        self.num_cells = num_cells

    def generate_netlist_bloc(self):
        template = ("subckt compound_synapse in_ter out_ter \n"
                    "parameters {} \n")

        parameters = " ".join(["seed{}".format(i+1) for i in range(self.num_cells)] +
                              ["PAP{}".format(i+1) for i in range(self.num_cells)])
        
        cells = ""
        for i in range(self.num_cells): #Here we define synapse terminals in a way to let MTJs T2 terminal node same as synapse's input node
            cell_line = ("\tcell{} (out_ter in_ter) cellPMAMTJ   param1=gl_STO   param2=gl_RV   param3=gl_T   param4=gl_Temp_var param7=RV_dev   "
                         "param5=PAP{}   param6=seed{}\n".format(i+1, i+1, i+1))
            cells += cell_line
        
        netlist_bloc = template.format( parameters) + cells + "ends compound_synapse\n"
        return netlist_bloc

class Input_neuron:
    """
    A class to specify a netlist bloc that describes an input neuron of the SNN, 
    a method takes a template, adds information of the current neuron 
    (neuron index, number of spikes associated to that input neuron, the duration of a single input spike, 
    and the duration of presenting an input example to the netowrk). That sting bloc will then be included
    in the final netlist.
 
    Attributes:
        input_index [int]: The index of this input neuron.
        n_spikes [int]: The number of spikes this neuron will generate.

    Methods
    -------
    generate_netlist_bloc():
        Generates a string bloc specefic to that input neuron in the final netlist file. 
    """

    def __init__(self, input_index, n_spikes):
        self.input_index = input_index
        self.n_spikes = n_spikes

    def generate_netlist_bloc(self):
        
        template = ( "input_neuron{} (input{} 0) Input_neuron r=0 n_spikes={} spike_duration=spike_duration presenting_time=sim_time \n") 
        return template.format(self.input_index, self.input_index, self.n_spikes)

class Output_neuron:
    """
    A class to specify a netlist bloc of an output neuron of the SNN, 
    a method takes a template, adds information of the current neuron 
    (neuron index, membrane threshold). That sting bloc will then be included
    in the final netlist.

    Attributes:
        output_index [int]: The index of this output neuron.


    Methods
    -------
    generate_netlist_bloc():
        Generates a string bloc specefic to that output neuron in the final netlist file. 
    """

    def __init__(self, output_index):
        self.output_index = output_index 

    def generate_netlist_bloc(self):
        template = ( "output_neuron{} (output{}) LIF_neuron mem_vth=mem_vth\n" )
        
        return template.format(self.output_index, self.output_index)

class Separator:
    """
    A class to seperate between componenets in the netlist for a better formatting.

    Methods
    -------
    generate_netlist_bloc():
        Generates a separation as a string.
    """

    def generate_netlist_bloc(self):
        return "\n//===================================================\n"     

class Netlist:
    """
    A class which assemles the instances of all the components, it then generates the netlist file
    add_component is a method that appends the instances of the componenets in one list called components.
    generate_netlist_file is a method that generates the diffrent parts of the netlist by using the generate_netlist_bloc()
    which is commun to all the components classes. 
    
    Attributes:
        file_path [str]: The path to the file where the netlist will be written.
        components [list]: The list of components instances (synapses, neurons, etc.).

    Methods
    -------
    add_component(component):
        appends the instance of each omponenent to the components list.
    generate_netlist_file():
        Writes the netlist to a file.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.components = [] # The netlist will be built inside this list

    def add_component(self, component):
        self.components.append(component)                       

    def generate_netlist_file(self):
        content = ""
        with open("netlist_ocn/netlist", "r") as file0:
            content += file0.read()

        for component in self.components:
            content += component.generate_netlist_bloc()        # use the class instances of componenets stroed in components to generate template and add it to content

        with open(self.file_path, "w") as file1:
            file1.write(content)


class NetworkGenerator:
    """
    The main class that generates all the netlist file, it is based on the Netlist class,
    It iterates over all the components by group of similar ones, it appends instances of 
    each component to the components list, while adding separation formatting between groups of similar components.

    Attributes:
        file_path [str]: The path to the file where the netlist will be written.
        num_input [int]: The number of input neurons in the network.
        num_output [int]: The number of output neurons in the network.
        num_cells [int]: The number of MTJ cells in each synapse.
        netlist [Netlist]: The netlist object that will be written to a file.
        n_spik_vec [list of int]: A list containing the number of spikes for each input neuron.

    Methods
    -------
    generate_netlist_file():
        similar to the generate_netlist_file of the Netlist class, but instead of generating a single component, 
        it operates globally, ie: it generates the whole netlist by iterating through the method of Netlist class.
    """

    def __init__(self, file_path, num_input, num_output, num_cells, n_spik_vec):
        self.file_path = file_path
        self.num_input = num_input
        self.num_output = num_output
        self.num_cells = num_cells
        self.netlist = Netlist(file_path)
        self.n_spik_vec = n_spik_vec # a list of a flattned array, containing n_spikes for each input neuron

    def generate_netlist_file(self):
        self.netlist.add_component(Synapse_subskt(self.num_cells))
        self.netlist.add_component(Separator())

        num_synapses = self.num_input * self.num_output
        
        # add the synapses 
        for i in range(1, num_synapses + 1):
            input_index = (i - 1) % self.num_input + 1
            output_index = (i - 1) // self.num_input + 1
            synapse = Synapse(input_index, output_index, self.num_cells)
            self.netlist.add_component(synapse)

        self.netlist.add_component(Separator())

        # add input neurons
        for i in range(1, self.num_input + 1):
            input_neuron = Input_neuron(i, self.n_spik_vec[i-1])
            self.netlist.add_component(input_neuron)

        self.netlist.add_component(Separator())

        # add output neurons 
        for i in range(1, self.num_output + 1):
            output_neuron = Output_neuron(i)
            self.netlist.add_component(output_neuron)

        self.netlist.generate_netlist_file()

