<details>
  <summary>Verilog-A model of Output neuron</summary>

```verilog
/*
Verilog-A model for leaky integrate-and-fire (LIF circuit)
Adapted from : "The Effects of Radiation on Memristor-Based Electronic 
Spiking Neural Networks." Dahl, Sumedha Gandharava (2020).
*/

`include "constants.vams"
`include "disciplines.vams"

// Start of the module
module LIF_neuron(nd_In) ; //, nd_cap);
  inout nd_In; 
 // output nd_cap;

//nd: node, bch: branch
  electrical nd_In, nd_switch, nd_charge, nd_cap, nd_gnd, Vth;
  branch (nd_In, nd_charge) bch_switch;
  branch (nd_charge, nd_cap) bch_charge;
  branch (nd_cap, nd_gnd) bch_discharge, bch_cap;

  // LIF circuit parameters
  parameter real Rcharge = 100e6 ; // charge resistance // 60
  parameter real Rdischarge =200e6 ; // discharge resistance
  parameter real Rpostdischarge = 10e3 ; // cap discharge during post spike
  parameter real mem_vth = 60e-3;        // neuron membrane potential threshold 

  // circuit connecting and disconnecting parameters
  parameter real Ron = 0 ; // connection valid, current flowing
  parameter real Roff = 1e300; // connection invalid, no current flowing

  //variables used
  real state, tfire, t, res_discharge, res_switch, V_fire;
  real membrane;

  // Start of the analog
  analog begin
    membrane = V(nd_cap);
    V(nd_gnd) <+ 0;
    V(Vth) <+ mem_vth; 
   
    // Start of the analysis
    if (analysis("ic")) begin
      state = 0;
      res_discharge = Roff;
      res_switch = Ron;
      //V_fire = 0;
      
    end else begin
      V(nd_switch) <+ V(nd_In); // separate circuit and LIF circuit
      V(bch_switch) <+ I(bch_switch) * res_switch; // (dis)connect LIC circuit
      V(bch_charge) <+ I(bch_charge) * Rcharge; // charges the LIF capacitor
      V(bch_discharge) <+ I(bch_discharge) * res_discharge; // discharges the cap
      I(bch_cap) <+ 300e-12*ddt(V(bch_cap));    //C =300pF
      
      // if vcap < vth, post-synaptic neuron is not firing
      if ((V(nd_cap) < V(Vth)) && (state == 0)) begin
        tfire = $abstime;
        res_switch = Ron; // connect LIC circuit
    
        if (V(nd_In) < V(nd_cap)) begin
          res_discharge = Rdischarge; // turn on cap discharge
          res_switch = Roff; // disconnect LIC circuit
        end
      end
      // if vcap > vth, post-synaptic neuron starts firing
      else begin
        res_discharge = Rpostdischarge; // turn on cap discharge
        res_switch = Roff; // disconnect LIC circuit
        state = 1; // set state to 1 for firing
        t = $abstime - tfire; // start timer for pulse width
   
        // start of the LIF spike
        // Potentiaion part
        if (t <= (0.5e-6)) begin
           V_fire = -100e-3/0.5e-6*t+150e-3;
           V(nd_In) <+ V_fire;
        end
        else if ((t > 0.5e-6 ) && (t <= 6.5e-6)) begin
           V_fire = -100e-3; 
           V(nd_In) <+ V_fire;
        end
        else if ((t > 6.5e-6 ) && (t <= 7e-6)) begin
           V_fire = (100e-3/0.5e-6)*(t-7e-6);
           V(nd_In) <+ V_fire;
        end
        // Depression part 
        else if ((t > 7e-6 ) && (t <= 7.2e-6)) begin
           V_fire = (100e-3/0.2e-6) * (t-7e-6);
           V(nd_In) <+ V_fire;
        end
        else if ((t > 7.2e-6 ) && (t <= 8.2e-6)) begin
           V_fire = 100e-3; 
           V(nd_In) <+ V_fire;
        end
        else if ((t > 8.2e-6 ) && (t <= 8.4e-6)) begin
           V_fire = (100e-3/0.2e-6)*(-t+8.4e-6);
           V(nd_In) <+ V_fire;
        end
        //TODO: refractory period
        else begin
           // Reset the voltage and set other variables
           V_fire = 0;
           V(nd_In) <+ V_fire;
           res_discharge = Roff; // turn off cap discharge
           res_switch = Ron; // turn on LIC switch
           state = 0; // set state to 0 for not firing
        end

      end // post-synaptic neuron ends firing
     
    end // End of the analysis
   end // End of the analog
endmodule // End of the module
```
</details>