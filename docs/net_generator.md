
Spice simulation with **Spectre** simulator requires a netlist file that includes the description of all the components of the circuit, and describes how these componenents are wired. The framework allows flexible geneartion of the netlist according to the desired networkd to be simulated. Only some network parameters should be given, for the corresponding netlist to be automatically generated.  The follwoing module `net_generator.py` which contains diffrent classes is responsible of generating the netlist. 
Circuit componenents are mangaged by the follwing classes : `Synapse`, `Synapse_subskt`, `Input_neuron`, `Output_neuron`, each contains a `generate_netlist_bloc` method that sets a string template bloc specific to that componenent and which should be added to the netlist file. 
The class `Netlist` concatinates the instances of the componenets in a list, and generates a string bloc of a single componenent ready to be inserted in the final netlist.
The class `NetworkGenerator` is the main class that assembles all the components by iterating the appending method of `Netlist` class. and trigers the netlist generation method of `Netlist`. 
Finally `Separotor` is a class to add a separation between a group of similar componenets for a bette rformatting.


::: src.net_generator

