class Synapse:
    """
    A class to specify a netlist bloc that describes an MTJ-based synapse of the SNN, 
    a method takes a template, adds information of the current synapse 
    (connected neurons, number of MTJs per synapse, initialized states, seeds,... )
    and adds it to the netlist. It uses as template the predefined compound_synapse 
    subcircuit .

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
        Generates a string bloc specefic to that synapse in the netlist file. 

    """

    def __init__(self, input_index, output_index, num_cells):
        self.input_index = input_index
        self.output_index = output_index
        #self.paps = [i%2 for i in range(num_cells)]   # alternate 0&1 in synapse
        self.paps = [random.randint(0, 1) for _ in range(num_cells)] #initialize randamely
        self.seeds = [random.randint(0, 9999) for _ in range(num_cells)]

    def generate_netlist_bloc(self):                 
        template = "synapse{}_{} (input{} output{}) compound_synapse "
        paps_str = " ".join("PAP{}={}".format(i + 1, pap) for i, pap in enumerate(self.paps))
        seeds_str = " ".join("seed{}={}".format(i + 1, seed) for i, seed in enumerate(self.seeds))
        return template.format(
            self.input_index, self.output_index, self.input_index, self.output_index
        ) + paps_str + " \\\n\t\t" + seeds_str + "\n"


class Input_neuron:
    """
    A class to specify a netlist bloc that describes an input neuron of the SNN, 
    a method takes a template, adds information of the current neuron 
    (neuron index, number of spikes associated to that neuron, spike_duration, presenting_time)
    and adds it to the netlist. 
 
    Attributes
    ----------
    input_index : int
        The index of this input neuron.
    n_spikes : int
        The number of spikes this neuron will generate.

    Methods
    -------
    generate_netlist_bloc():
        Generates a string representing the SPICE netlist bloc for this input neuron.
    """

    def __init__(self, input_index, n_spikes):
        self.input_index = input_index
        self.n_spikes = n_spikes

    def generate_netlist_bloc(self):
        
        template = ( "input_neuron{} (input{} 0) Input_neuron r=0 n_spikes={} spike_duration=spike_duration presenting_time=sim_time \n") 
        return template.format(self.input_index, self.input_index, self.n_spikes)

class Output_neuron:
    """
    A class to represent an Output Neuron in a Spiking Neural Network (SNN).

    Attributes
    ----------
    output_index : int
        The index of this output neuron.

    Methods
    -------
    generate_netlist_bloc():
        Generates a string representing the SPICE netlist block for this output neuron.
    """

    def __init__(self, output_index):
        self.output_index = output_index 

    def generate_netlist_bloc(self):
        template = ( "output_neuron{} (output{}) LIF_verilog_extcap mem_vth=mem_vth\n" )
        
        return template.format(self.output_index, self.output_index)


class Synapse_subskt:
    """
    A class to represent a Synapse Subcircuit in a Spiking Neural Network (SNN).

    Attributes
    ----------
    num_cells : int
        The number of MTJ cells in each synapse.

    Methods
    -------
    generate_netlist_bloc():
        Generates a string representing the SPICE netlist block for this synapse subcircuit.
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

class Separator:
    """
    A class to represent a Separator in a SPICE netlist.

    Methods
    -------
    generate_netlist_bloc():
        Generates a string representing the SPICE netlist block for this separator.
    """

    def generate_netlist_bloc(self):
        return "\n//===================================================\n"     

class Netlist:
    """
    A class to represent a SPICE Netlist.

    Attributes
    ----------
    file_path : str
        The path to the file where the netlist will be written.
    components : list
        The list of components (synapses, neurons, etc.) in the netlist.

    Methods
    -------
    add_component(component):
        Adds a component to the netlist.
    generate_netlist_file():
        Writes the netlist to a file.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.components = []

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
    A class to generate a SPICE netlist for a Spiking Neural Network (SNN).

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
        Generates the SPICE netlist for the SNN and writes it to a file.
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

        for i in range(1, num_synapses + 1):
            input_index = (i - 1) % self.num_input + 1
            output_index = (i - 1) // self.num_input + 1
            synapse = Synapse(input_index, output_index, self.num_cells)
            self.netlist.add_component(synapse)

        self.netlist.add_component(Separator())

        for i in range(1, self.num_input + 1):
            input_neuron = Input_neuron(i, self.n_spik_vec[i-1])
            self.netlist.add_component(input_neuron)

        self.netlist.add_component(Separator())

        for i in range(1, self.num_output + 1):
            output_neuron = Output_neuron(i)
            self.netlist.add_component(output_neuron)

        self.netlist.generate_netlist_file()
