class Synapse:
    """
    A class to specify a netlist bloc that describes an MTJ-based synapse of the SNN, 
    a method takes a template, adds information of the current synapse 
    (connected neurons, number of MTJs per synapse, initialized states, seeds,... )
    and adds it to the netlist. Each synapse calls a compound_synapse subcircuit which
    is added once to the netlist with annother class. 

    Attributes
    ----------
    input_index : int
        The index of the input neuron connected to this synapse.
    output_index : int
        The index of the output neuron connected to this synapse.
    paps : list of int
        The list of initial states of free layers for each MTJ in the synapse. (0 parallel, 1 anti-parallel)
    seeds : list of int
        The list of seed values used for stochasticity for each MTJ in the synapse.

    Methods
    -------
    generate_netlist_bloc():
        Generates a string bloc specefic to that synapse in the final netlist file. 

    """

    def __init__(self, input_index, output_index, num_cells):
        self.input_index = input_index
        self.output_index = output_index
        #self.paps = [i%2 for i in range(num_cells)]                 # alternate 0&1 in the MTJs of the synapse
        self.paps = [random.randint(0, 1) for _ in range(num_cells)] #initialize randamely
        self.seeds = [random.randint(0, 9999) for _ in range(num_cells)]

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
    which will be called by all the synapsesi. It is composed of multiple MTJs (the number is given as attribute), 
    and it makes call of the cellPMAMTJ subcircuit which is predefined in the initial netlist file.
    A method takes a template, adds parameters to it : either to set stochasticity, variability,
    temperature and its variation or not, and sets as parameters the initial state of the MTJ, and the seed. 
    It then adds the string bloc of the synapse subcircuit only once to the final netlist. 

    Attributes
    ----------
    num_cells : int
        The number of MTJ cells in each synapse.

    Methods
    -------
    generate_netlist_bloc():
        Generates a string bloc specefic to the compound_synapse subcircuit in the final netlist file. 
    """

    def __init__(self, num_cells):
        self.num_cells = num_cells

    def generate_netlist_bloc(self):
        template = ("subckt compound_synapse ter1 ter2 \n"
                    "parameters {} \n")

        parameters = " ".join(["seed{}".format(i+1) for i in range(self.num_cells)] +
                              ["PAP{}".format(i+1) for i in range(self.num_cells)])
        
        cells = ""
        for i in range(self.num_cells):
            cell_line = ("\tcell{} (ter1 ter2) cellPMAMTJ   param1=gl_STO   param2=gl_RV   param3=gl_T   param4=gl_Temp_var   "
                         "param5=PAP{}   param6=seed{}\n".format(i+1, i+1, i+1))
            cells += cell_line
        
        netlist_bloc = template.format( parameters) + cells + "ends compound_synapse\n"
        return netlist_bloc

class Input_neuron:
    """
    A class to specify a netlist bloc that describes an input neuron of the SNN, 
    a method takes a template, adds information of the current neuron 
    (neuron index, number of spikes associated to that input neuron, the duration of a single input spike, 
    and the duration a single example is presented to the netowrk). It then adds the string bloc of that neuron 
    to the netlist. 
 
    Attributes
    ----------
    input_index : int
        The index of this input neuron.
    n_spikes : int
        The number of spikes this neuron will generate.

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
    (neuron index, membrane threshold). It then adds the string bloc of that neuron 
    to the netlist. 

    Attributes
    ----------
    output_index : int
        The index of this output neuron.

    Methods
    -------
    generate_netlist_bloc():
        Generates a string bloc specefic to that output neuron in the final netlist file. 
    """

    def __init__(self, output_index):
        self.output_index = output_index 

    def generate_netlist_bloc(self):
        template = ( "output_neuron{} (output{}) LIF_verilog_extcap mem_vth=mem_vth\n" )
        
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
    A class used to assemble a class instnace definition of each component, and put them together in a list called components,
    it appends the components instances iterativeley, it then uses a method to generate a netlist file based on the instances 
    in the components list.
    
    Attributes
    ----------
    file_path : str
        The path to the file where the netlist will be written.
    components : list
        The list of components instances (synapses, neurons, etc.)

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
    It iterates over all the components by group of similar ones, it appends the Netlist instance of 
    each component to the components list, while adding separation formatting between groups of similar components.

    Attributes
    ----------
    file_path : str
        The path to the file where the netlist will be written.
    num_input : int
        The number of input neurons in the network.
    num_output : int
        The number of output neurons in the network.
    num_cells : int
        The number of MTJ cells in each synapse.
    netlist : Netlist
        The netlist object that will be written to a file.
    n_spik_vec : list of int
        A list containing the number of spikes for each input neuron.

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
