# MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
> This projects build on [Part I - Site Assessment](https://github.com/aa-sharma/micro_hydro_bc) where we identified candidate locations for a micro-hydropower plant in rural Southwest British Columbia. In this project, we assume a capacity of 100kW for the candidate site and conduct a radial distribution feeder impact study through load flow, voltage rise analysis, and reverse power flow check under steady-state and fault conditions.
The grid integration loosely follows [BC Hydro's Distributed Generation Technical Interconnection Requirements - 100 kW and Below (DGTIR-100)](https://www.bchydro.com/content/dam/BCHydro/customer-portal/documents/distribution/standards/ds-dgi-100kw-and-below-requirements.pdf)

 <img src="bc-hydro-integration.png" width="50%">

## System Definition
* 1 slack bus (utility substation)
* 1 feeder (radial)
* 3 loaded buses (representing residential/rural demand)
* 1 generator bus (100kW micro-hydro)
* 1 transformer (steps voltage up from 480V to 12.47kV)

 <img src="topo.png" width="40%">

               
### Design Simplifications and Assumptions
* Constant power loads (PQ)
* Typical line imepedance values
* Balanced 3-phase system
* Harmonics are ignored

### Generator & Transformer Attributes
The following attributes are assumed for the 100kW micro-hydro power plant:
* Power Rating: 100kW
* Voltage: 480V (3-phase)
* Frequency: 60Hz (synchronized with local BC Hydro grid standards)
* Generator Type: Asynchronous generator
* Step-up Transformer: 0.48kV -> 12.47kV, 150kVA


## Areas of Study
1. Power flow (Voltage profile)
2. Reverse power flow check
3. Transformer behaviour
4. Short-circuit analysis

## Power Flow
"Power Flow Analysis is considered the backbone of modern power systems because it plays a vital role in ensuring the grid's reliable, efficient, and safe operation. By providing a detailed assessment of power Generation, Transmission and distribution, Load Flow Analysis helps engineers optimize system performance, maintain voltage stability, and reduce power losses. It also serves as a foundation for other advanced power system studies, such as harmonic analysis and stability assessments."

1. Voltage Profile: Ensuring that voltage levels across all buses remain within tolerable limits.
2. Real Power Loss Minimization: Identifying and reducing energy losses in transmission lines and transformers.
3. System Optimization: Optimizing the capital investment by optimally selecting the equipment ratings and their configurations

The Newton-Raphson method is used by the program in this study.

<img src="power-flow-problem-table.png" width="75%">

<img src="power-flow-equations1.png" width="75%">

<img src="power-flow-equations2.png" width="75%">


Case 1: Generator OFF (baseline voltage profile)

Case 2: Partial generation (30% i.e. 30kW)

Case 3: Partial generation (60% i.e. 60kW)

Case 4: Generator ON (100% i.e. 100kW)



## Simulation
Simulations performed in python using [pandapower](https://pandapower.readthedocs.io/en/latest/powerflow/ac.html)

### Outputs

Single Line Diagram

<img src="outputs/single-line-diagram.png" width="100%">

Voltage Profiles

<img src="outputs/voltage_profile/voltage_profile_gen_off.png" width="100%">
<img src="outputs/voltage_profile/voltage_profile_gen_30.png" width="100%">
<img src="outputs/voltage_profile/voltage_profile_gen_60.png" width="100%">
<img src="outputs/voltage_profile/voltage_profile_gen_100.png" width="100%">


Voltage Angles

<img src="outputs/voltage_angle/voltage_angle_gen_off.png" width="100%">
<img src="outputs/voltage_angle/voltage_angle_gen_30.png" width="100%">
<img src="outputs/voltage_angle/voltage_angle_gen_60.png" width="100%">
<img src="outputs/voltage_angle/voltage_angle_gen_100.png" width="100%">

Line Loading

<img src="outputs/line_loading/line_loading_gen_off" width="100%">
<img src="outputs/line_loading/line_loading_gen_30" width="100%">
<img src="outputs/line_loading/line_loading_gen_60" width="100%">
<img src="outputs/line_loading/line_loading_gen_100" width="100%">


Transfomer Loading
<img src="outputs/transformer_loading/transformer_loading_gen_off.png" width="100%">
<img src="outputs/transformer_loading/trafo_loading_gen_30.png" width="100%">
<img src="outputs/transformer_loading/transfo_loading_gen_60.png" width="100%">
<img src="outputs/transformer_loading/trafo_loading_gen_100.png" width="100%">


