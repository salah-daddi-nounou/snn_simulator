<details>
  <summary>Verilog-A model of input neuron</summary>

```verilog

`include "constants.vams"
`include "disciplines.vams"

module Input_neuron(terminal1, terminal2);
  inout terminal1, terminal2; 
  electrical terminal1, terminal2;
  voltage V_neuron;
  parameter real r=0 from [0:inf);
 
  parameter real n_spikes = 2 ;             // It represents the neuron intensity
  parameter real spike_duration = 60e-3 ;   // Maximum duration of a single spike
  parameter real presenting_time = 300e-3;  // The total time a pixel is presented to the network
  real slope = -(150-(-90))*1e-3/spike_duration; // slpe of input spike
  real t_window = presenting_time/n_spikes; // window includes presentime_time + itme between two spikes 
  real t_;
  real t0, spiking;

  analog begin
  
    if (analysis("ic")) begin     // initial conditions
      V(V_neuron) <+ 0;
      t_ = 0;
      spiking = 0;

    end else begin                // Analysis begin
      if (spiking == 0) begin     // start spiking 
        t0 = $abstime;
        spiking = 1; 
        V(V_neuron) <+ 150e-3;
      end else begin              // it is already spiking
        t_ = $abstime - t0;

        if (t_ <= t_window && t_ <= spike_duration) begin
          V(V_neuron) <+ slope*t_+150e-3; 
        end else if (t_ > spike_duration && t_ <= t_window) begin
          V(V_neuron) <+ 0;
        end else begin
          spiking = 0;
          t_ = 0;
          V(V_neuron) <+ 150e-3;
        end
      end                       // End spiking 
    end // End of the analysis
    V( terminal1, terminal2) <+ r*I( terminal1, terminal2)+ V(V_neuron);

   end // End of the analog
endmodule // End of the module

```
</details>