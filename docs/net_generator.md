
The simulation needs a netlist file where all the circuit components are described and the wiring between them is precised. 

The framework allows flexible geneartion of the netlist according the desired networkd to be simulated. Only some network parameters should be given, so that the corresponding netlist is automatically generated.  The module net_generator.py which contains diffrent classes is responsible of generating the netlist. 

Component classes are : Synapse, Synapse_subskt, Input_neuron, Output_neuron, each contains a generate_netlist_bloc method that sets the templat specific to taht componenent that should be added to the netlist file. 

The class Netlist concatinates the instances of the componenets in a list, and generates a string bloc of a single componenent ready to be inserted in the final netlist.

The class NetworkGenerator is the main class that assembles all the components by iterating the method of Netlist class. 

Finally Separotor is a class to add a separation between a group of similar componenets for a bette rformatting 
::: src.net_generator
