<details>
  <summary>Verilog-A model of MTJ device</summary>

```verilog
/* Copyright @ 2018 Fert Beijing Institute, BDBC and School of Electronic and Information Engineering, Beihang Univeristy, Beijing 100191, China
The terms under which the software and associated documentation (the Software) is provided are as the following:
The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the Software or the use or other dealings in the Software.
The authors or copyright holders grants, free of charge, to any users the right to modify, copy, and redistribute the Software, both within the user's organization and externally, subject to the following restrictions:
1. The users agree not to charge for the code itself but may charge for additions, extensions, or support.
2. In any product based on the Software, the users agree to acknowledge the Research Group that developed the software. This acknowledgment shall appear in the product documentation.
3. The users agree to reproduce any copyright notice which appears on the software on any copy or modification of such made available to others.
Agreed to by 
You WANG, Yue Zhang, Weisheng Zhao, Lirida Alves de Barros Naviner, Hao Cai and Jaques-Olivier Klein

//Title: Compact model of Perpendicular Magnetic Anistropy (PMA) MTJ based on Spin transfer torque mechanism
//Version: Beta.4.5
//Date:20 April 2020
//Language: VerilogA

-------------------------------------------
In this model, it takes into account the static, dynamic and stochastic behavoirs of PMA MTJ nanopillar
1.MTJ resistance calculation based on brinkman model
2.TMR dependence on the bias voltage
3.Spin polarity calculation model for magnetic tunnel junction
4.Critical current calculation 
5.Dynamic model (>critical current, also sun's model)
6.Stochastic model 
7.Resistance variation
8.Temperature evaluation
-------------
Modified by Salah DADDINOUNOU
// Optimized the code and removed redundancy.
// Signal ix is set to 0 or 1 not 0 or -1 (it was set negative to indecate that the current flows out, when there were a probing termnial)
// Removed the probing terminals because the framework allows direct access to signals. Removed also temp terminal.   
*/
/*--------------------The parameters are from the prototypes of Univ. Tohuku-------------------*/

`resetall
`include "constants.vams"
`include "disciplines.vams"
`define explimit 85.0
`define exp(x) exp(min(max((x),-`explimit),`explimit))
`define sqrt(x) pow( (x), 0.5)

`define rec 1        	//Shape definition
`define ellip 2
`define circle 3

/*----------------------------Electrical Constants-----------------------------*/ 
/*----------Elementary Charge---------------*/
`define e 1.6e-19
/*----------Bohr Magnetron Costant----------*/
`define ub 9.27e-28
/*----------Boltzmann Constant------------- */ 
`define Kb 1.38e-23
/*----------Electron Mass------------- */ 
`define m 9.10e-31
/*----------Euler's constant---------------*/ 
`define C 0.577


module Model(T1,T2);
inout T1, T2;
electrical T1, T2;
electrical n1,n2; //virtual terminals of RC circuit for temperature evaluation 
/*----------Ttrans=store the state of the MTJ with time influence, non-volatile way------------- */

/*--------------------MTJ Technology Parameters(Corresponds to the HITACHI MTJ Process)-------------*/ 

/*----------Gilbert Damping Coefficient---------------*/
parameter real alpha=0.027;
/*----------GyroMagnetic Constant in Hz/Oe---------------*/
parameter real gamma=1.76e7;
/*----------Electron Polarization Percentage % ---------------*/ 
parameter real P=0.52;
/*----------Out of plane Magnetic Anisotropy in Oersteds---------------*/ 
parameter real Hk=1433;
/*----------Saturation Field in the Free Layer in Oersteds---------------*/
parameter real Ms=15800;
/*----------The Energy Barrier Height for MgO in electron-volt---------------*/ 
parameter real PhiBas=0.4;
/*----------Voltage bias when the TMR(real) is 1/2TMR(0) in Volt---------------*/ 
parameter real Vh=0.5; //experimental value with MgO barrier

/*--------------Device Parameters(Corresponds to the HITACHI 240 x 80 MTJ)--------------------------*/ 

/*----------Height of the Free Layer in nm---------------*/
parameter real tsl=1.3e-9 from[0.7e-9:3.0e-9];
/*----------Length in nm---------------*/
parameter real a=32e-9;
/*----------Width in nm---------------*/
parameter real b=32e-9;
/*----------Radius in nm---------------*/
parameter real r=16e-9;
/*----------Height of the Oxide Barrier in nm---------------*/ 
parameter real tox=8.5e-10 from[8e-10:15e-10]; 
/*----------TMR(0) with Zero Volt Bias Voltage ---------------*/ 
parameter real TMR=0.7;

/*----------Shape of MTJ---------------*/
parameter real SHAPE=3 from[1:3];    // 1:rectangle  2:ellipse 3:circle
/*----------Neel-Brown model parameter ---------------*/
parameter real tau0=8.7e-10; //experiental value, prototype Hitachi 2007m with CoFe layer 
/*----------Error probability Ps=1-Pr(t) ----------------*/
parameter real Ps=0.999999;
/*----------Threshold for Neel-Brown model----------------*/
parameter real brown_threshold_AP2P=0.15;   
parameter real brown_threshold_P2AP=0.1;   

/*----------MTJ State Parameters----------------*/
/*----------Initial state of the MTJ, 0 = parallele, 1 = anti-parallele----*/ 
parameter integer PAP=1 from[0:1]; 
/*----------Room temperature in Kelvin----------------*/
parameter real T= 300;
/*----------Resistance area product in ohmum2----------------*/ 
parameter real RA=5 from[5:15];

/*----------Parameters of RC circuit for time modelisation for temperature---------------*/
parameter integer Temp_var=0 from[0:1]; //choice of temperature fluctuation
/*----------Heat capacity per unit volume in J/m3*K----------------*/
parameter real Cv= 2.74e6 from[2.735e6:2.7805e6];
/*----------Thermal conductivity of the thermal barrier(MgO) in W/m*K----------------*/ 
parameter real lam= 84.897 from [84.8912:84.9449];
/*----------Total thickness of MTJ nanopillar in nm----------------*/
parameter real thick_s= 3.355e-8;

/*----------RC circuit for time modelisation for temperature---------------*/ 
parameter real resistor=100e6;
parameter real coeff_tau=12; 	//Coefficient to increase tau_th
real capacitor; 				//virtual capacitor
real tau_th; 					//characteristic heating/cooling time
real temp; 						//real temperature of MTJ
real temp_init; 				//temperature initialised
real R; 						//resistance of MTJ

/*---------Parameters for stochasticity and variability behaviors---------------*/
parameter integer STO=0 from[0:2];  	    // stochasticity: 0=no stochastic, 1=random exponential distribution, 2=random gauss distribution
parameter integer RV=0 from[0:2]; 	        // process varibility: 0 no var, 1 random uniform distribution,2 random gauss distribution
parameter real dev = 0;                     // intermediate std parameter to be used bellow
parameter real DEV_tox=dev; //0.03; 		// variability std for gauss distribution(RV=2) of tox (oxide thickness) 
parameter real DEV_tsl=dev; //0.03; 		// variability std for gauss distribution(RV=2) of tsl (FL thickness)
parameter real DEV_TMR=dev; //0.03;		    // variability std for gauss distribution(RV=2) of TMR 
parameter real STO_dev=1;                   // stochasticity std for gauss distribution(STO=2) of duration		

/*------------------------------------variables-------------------------------------*/

//Polaristion constant for the two states of STT-MTJ
real PolaP;			//Polarization state parallel of STT-MTJ
real PolaAP;		//Polarization state anti-parallel of STT-MTJ
real surface;		//Surface of MTJ
real gp; 			//Critical current density for P state 
real gap; 			//Critical current density for AP state
real Em,EE;			//Variable of the Slonczewski model
real TMRR;			//TMR real value for P state
real TMRRT;			//TMR real value for AP state
real Ro; 			//Resistance of MTJ when bias voltage = 0V 
real Rap; 			//Resistance value for AP state 
real Rp; 			//Resistance value for P state

//Voltage of MTJ
real Vb; 			//V(T1,T2) = V(T1) - V(T2)  When positive, it can switch P2AP 
real Vc; 			//V(T2,T1) = V(T2) - V(T1)  When positive, it can switch AP2P 
real Id; 			//Current of MTJ

//critial current for the two states of STT-MTJ
real IcAP; 			//Critial current for AP state
real IcP; 			//Critial current for P state
real ix; 			//Current used to store the state of the MTJ (0: parallel, 1: anti-parllel) 
real tau; 			//Probability parameter
real FA; 			//Factor for calculating the resistance based on RA

/*--------Stochastic effects--------------*/

real durationstatic, duration; 		//time needed to be sure that the switching is effected
real toxreal;						//real thickness of oxide layer		
real tslreal;						//real thickness of free layer		
real TMRreal;						//real TMR

parameter integer mtj_seed = 0;	    // device-specific seed generated by python to be used for both variability and stochasti 
integer seed1=0;   					// seed for process variability random distributions 
integer seed2=0;   					// seed for stochasticity random distributions  

/*----------switching delay----------------*/
real P_APt;
real AP_Pt;
real NP_APt,NAP_Pt;

integer counter;
integer fp;
//--------------------------------------------------------------------------------------------------------------------------------------//

analog begin

if (SHAPE==1)				//square
begin
	surface=a*b;
end
else if (SHAPE==2) 			//ellipse (a/2 and b/2 are semi-minor & semi-major)
begin
	surface=`M_PI*a*b/4;
end
else 						// round
begin
	surface=`M_PI*r*r;		
end

Vc=V(T2,T1);
Vb=V(T1,T2);

@(initial_step) begin
	counter=0;
	FA=3322.53/RA;			    // initialization of resistance factor according to RA product
	seed1 = mtj_seed;	        // process variability MC
	seed2 = mtj_seed;	        // stochasticity MC

	if (RV==1)						//real thinkness of oxide layer, free layer and real TMR with uniform dist variability
	begin
		toxreal=$rdist_uniform(seed1,(tox-tox*DEV_tox),(tox+tox*DEV_tox));
		tslreal=$rdist_uniform(seed1,(tsl-tsl*DEV_tsl),(tsl+tsl*DEV_tsl));
		TMRreal=$rdist_uniform(seed1,(TMR-TMR*DEV_TMR),(TMR+TMR*DEV_TMR));			
	end
	else if (RV==2)					//real thinkness of oxide layer, free layer and real TMR with gauss dist variability 
	begin
		toxreal=abs($rdist_normal(seed1,tox,tox*DEV_tox));
		tslreal=abs($rdist_normal(seed1,tsl,tsl*DEV_tsl));
		TMRreal=abs($rdist_normal(seed1,TMR,TMR*DEV_TMR));										
	end
	else
	begin							// No variability 
		toxreal=tox;
		tslreal=tsl;
		TMRreal=TMR;
	end
	// parameters for temperature
	temp=T;
	temp_init=T;	
	tau_th= Cv*thick_s / (lam/thick_s);	
	capacitor=coeff_tau*tau_th/resistor;

	Ro=(toxreal*1.0e10/(FA*`sqrt(PhiBas)*surface*1.0e12))*exp(1.025*toxreal*1.0e10*`sqrt(PhiBas));		// Ro : Resistance of MTJ when bias voltage = 0V
	//parameters for calculating switching delay
	Em=Ms*tslreal*surface*Hk/2;      // Em : Variable of the Slonczewski model
	duration=0.0;
	P_APt=1e9;
	AP_Pt=1e9;
	NP_APt=1e9;
	NAP_Pt=1e9;
	
	if(analysis("dc"))	//States inititialisation
	begin
		ix=PAP;	   		// ix: Current used to store the state of the MTJ    
	end
	else
	begin
		ix=PAP;
	end	
end 					//end of initial_step

if(Temp_var==0)			//temperature is constant
begin
    temp=temp_init; 
end
else					//temperature actualisation
begin
    temp=V(n2) + temp_init;
end      
EE=Em/(`Kb*temp*40*`M_PI);  

/*----calculation of real current------*/

TMRR=TMRreal/(1+Vb*Vb/(Vh*Vh));	
Rp=Ro;
Rap=Rp*(1+TMRR);
if(ix==0)
begin
	R=Rp;
end
else    //ie: ix=1 if dc and ix =-1 for tran
begin
	R=Rap;
end
 
Id=Vb/R;

/*----calculation of rcritical current------*/

PolaP=`sqrt(TMRreal*(TMRreal+2))/(2*(TMRreal+1));			//Polarization state parallel
gp=alpha*gamma*`e*Ms*tslreal*Hk/(40*`M_PI*(`ub*PolaP)); 	//Critical current density    
IcP=gp*surface;												// Critical current for P state
PolaAP=`sqrt(TMRreal*(TMRreal+2))/(2*(TMRreal+1));			//Polarization state anti-parallel  
gap=alpha*gamma*`e*Ms*tslreal*Hk/(40*`M_PI*(`ub*PolaAP));	//Critical current density  
IcAP=gap*surface; 											// Critical current for AP state		 

/*------Counter of time when real current is higher than critical current */

@(above(Id-IcP,+1))   
begin
	P_APt = $abstime;
	NP_APt=1e9;		
end

@(above(-Id-IcAP,+1))
begin
	AP_Pt = $abstime;
	NAP_Pt=1e9;  	
end

@(above(Vb-brown_threshold_P2AP,+1))
begin
	NP_APt = $abstime;
	AP_Pt=1e9;
	NAP_Pt=1e9;	
end

@(above(Vc-brown_threshold_AP2P,+1))
begin
	NAP_Pt = $abstime;
	P_APt=1e9;
	NP_APt=1e9;  	
end
//-------------------
if(analysis("dc")) 					 // dc analysis                 
begin	
	if(ix==0)
	begin
		if(Vb>=(IcP*Rp))		
		begin
			ix=1.0;
		end
	end
	else 	//(ix==1)
	begin				
		if(Vc>=(IcAP*Rap))
		begin
			ix=0.0;
		end
	end
    I(T1,T2)<+Id;						//Actualisation of the current of MTJ with the value calculated
end				
//------------------------------------------------------------------------------------------------------------------------------
else    								// transient analysis                 
begin
	if(ix==0)       				// parallel state
	begin	

		if(Vb>=IcP*Rp)				//Current higher than critical current, dynamic behavior: Sun model 
		begin
			durationstatic=(`C+ln(`M_PI*`M_PI*(Em/(`Kb*temp*40*`M_PI))/4))*`e*1000*Ms*surface*tslreal*(1+P*P)/(4*`M_PI*2*`ub*P*10000*abs(Id-IcP));	//Average time needed for switching
			if(STO==1)				//parallel -- Vb > Icp *Rp -- expon_ stochast
			begin
				duration=abs($rdist_exponential(seed2, durationstatic)); 
			end
			else if(STO==2)			//parallel -- Vb > Icp *Rp -- normal_ stochast
			begin					  
				duration=abs($rdist_normal(seed2,durationstatic,durationstatic*STO_dev));
			end	
			else					//parallel -- Vb > Icp *Rp -- NO stochast
			begin			
				duration=durationstatic;
			end							
			
			if(duration<=($abstime-P_APt))  // duration is enough to switch  //Switching of the free layer always occurs
			begin
				ix=1.0;	     // change of the current state of MTJ	
			end
			else
			begin
				ix=0.0;
			end
		end
		else						// current smaller than critical current : Neel-Brown model
	    
        if(Vb>brown_threshold_P2AP)	//added
		begin
			ix=0.0;
			tau=tau0*exp(Em*(1-abs(Id/IcP))/(`Kb*temp*40*`M_PI));	
			if(Vb>brown_threshold_P2AP)	
			begin
				if (Vb<0.8*IcP*Rp)
				begin
					if(STO==1) 
					begin
						duration=abs($rdist_exponential(seed2, tau));
					end
					else if(STO==2)
					begin
				    	duration=abs($rdist_normal(seed2,tau,tau*STO_dev));
					end		
					else
					begin
						duration=tau;			
					end										
                   	if (($abstime-NP_APt) >= duration)	
					begin
						ix=1.0;  
					end
					else
					begin
						ix=0.0;
					end
				end 			
			end		
		end
	
	end 		// end of parallel state
	//-----------------------------------------------------------------------------		
	else       // initial state anti-parallel
    begin

	   	if(Vc>=(IcAP*Rap)) // anti-parallel, current higher than critical current: Sun model
		begin
			durationstatic=(`C+ln(`M_PI*`M_PI*(Em/(`Kb*temp*40*`M_PI))/4))*`e*1000*Ms*surface*tslreal*(1+P*P)/(4*`M_PI*2*`ub*P*10000*abs(-Id-IcAP));
			if(STO==1)
			begin
				duration=abs($rdist_exponential(seed2, durationstatic));
			end
			else if(STO==2)
			begin
				duration=abs($rdist_normal(seed2,durationstatic,durationstatic*STO_dev));		
			end
			else
			begin
				duration=durationstatic;
			end
			if(duration<=($abstime-AP_Pt))
			begin
				ix=0.0;		
	       	end 
			else 		// duration is not enough to switch
			begin
				ix=1.0;
			end
		
		end 		
		else			// trans - stochastic - anti-parallel - Neel Brwon 

	    if(Vc>brown_threshold_AP2P)	//added
		begin
			tau=tau0*exp(Em*(1-abs(Id/IcAP))/(`Kb*temp*40*`M_PI));
			if(Vc>brown_threshold_AP2P)	
			begin
				if (Vc<0.8*IcAP*Rap)
				begin
					if(STO==1)
					begin				
						duration=abs($rdist_exponential(seed2, tau));
                   	end
					else if(STO==2)
					begin
						duration=abs($rdist_normal(seed2,tau,tau*STO_dev));
					end					
					else
					begin
						duration=tau;
					end	
					if (duration<=($abstime-NAP_Pt))
                    begin 
						ix=0.0;	
                   	end
					else
					begin
						ix=1.0;
					end
				end
			end
		end

	end    	//end of ant-parallel state 
//-------------------------------------------------------------------------------------------------------------
	
    I(T1,T2)<+Id;           
end  // end of transiant simulation 

//-------------------------------------------------------------------------------------------------------------

if(Temp_var==1)
begin      
	V(n1) <+ ( V(T1,T2)*V(T1,T2) )/ ( 2*R*surface*lam/(thick_s-toxreal));   
	I(n1,n2) <+ V(n1,n2) / resistor;
	I(n2) <+ capacitor * (ddt(V(n2)));
end

@(final_step) begin
//$fclose(fp);
end

end // end of the analog begin 

endmodule
```
</details>