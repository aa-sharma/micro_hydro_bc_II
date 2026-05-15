# MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
> This projects build on [Part I - Site Assessment](https://github.com/aa-sharma/micro_hydro_bc) where we identified candidate locations for a micro-hydropower site in rural Southwest British Columbia. In this project, we assume a capacity of 100kW for the candidate site and conduct a radial distribution feeder impact study through load flow, voltage rise analysis, and reverse power flow check under steady-state and fault conditions.

## System Definition
* 1 slack bus (utility substation)
* 1 feeder (radial)
* 4-6 loaded buses (representing residential/rural demand)
* 1 generator bus (100kW micro-hydro)
* aggregated loads

Structure

 <img src="topo.png" width="30%">

## Areas of Study
1. Power flow (Voltage impact study)
2. Reverse power flow
3. Transformer behaviour
4. Short-circuit analysis

## Power Flow
Case 1: Generator OFF (baseline voltage profile)

Case 2: Generator ON (100kW generation)

Case 3: Partial generation (30%, 60%)


## Simulation
Simulations performed in python using pandapower
https://www.pandapower.org/start/

### Design Simplifications and Assumptions
* Constant power loads (PQ)
* Typical line imepedance values
* Balanced 3-phase system
* Harmonics are ignored
