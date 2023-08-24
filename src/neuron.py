`include "disciplines.vams"

module LeakyIntegrateAndFire (
  input voltage_in,
  inout shared_inhibit,
  output spike_out
);

  // Parameters
  parameter real R = 1.0;         // Membrane resistance (Ohms)
  parameter real C = 1.0;         // Membrane capacitance (Farads)
  parameter real Vth = 1.0;       // Threshold voltage (Volts)
  parameter real Vreset = 0.0;    // Reset voltage (Volts)
  parameter real refractory_period = 1.0;   // Refractory period (Seconds)

  // Internal Variables
  real Vm;       // Membrane voltage (Volts)
  real Imem;     // Membrane current (Amps)
  real t_last_spike;    // Time of last spike (Seconds)

  // Initial Conditions
  initial begin
    Vm = 0.0;
    Imem = 0.0;
    t_last_spike = -refractory_period;
  end

  // Continuous Time Behavior
  analog begin
    // Check if refractory period has passed
    if (time - t_last_spike > refractory_period) begin
      // Membrane current equation
      Imem = (voltage_in - Vm) / R;

      // Membrane voltage equation
      ddt(Vm) = Imem / C;

      // Spike generation
      if (Vm >= Vth) begin
        spike_out = 1;
        Vm = Vreset;
        t_last_spike = time;
        shared_inhibit = 1;
      end
      else begin
        spike_out = 0;
        //shared_inhibit = 0;
      end
    end
    else begin
      // During refractory period, no accumulation or spike generation
      Imem = 0;
      ddt(Vm) = 0;
      spike_out = 0;
      //shared_inhibit = 0;
    end
    
    // Inhibition
    if (shared_inhibit) begin
      Vm = 0;
    end
  end

endmodule

