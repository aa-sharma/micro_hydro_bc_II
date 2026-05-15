# MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
> This projects build on [Part I - Site Assessment](https://github.com/aa-sharma/micro_hydro_bc) where we identified candidate locations for a micro-hydropower site in rural Southwest British Columbia. In this project, we assume a capacity of 100kW for the candidate site and conduct a radial distribution feeder impact study through load flow, voltage rise analysis, and reverse power flow check under steady-state and fault conditions.

## System Definition
* 1 slack bus (utility substation)
* 1 feeder (radial)
* 4-6 loaded buses (representing residential/rural demand)
* 1 generator bus (100kW micro-hydro)
* aggregated loads

Structure:
Slack (12.47 kV)
   |
 Bus 1
   |
 Bus 2
   |
 Bus 3  ← 100 kW Micro-Hydro
   |
 Bus 4 (load end)

## Areas of Study
1. Power flow (Voltage impact study)
2. Reverse power flow
3. Transformer behaviour
4. Short-circuit analysis

## Power Flow
Case 1: No generation (normal load flow)

Case 2: Generator ON (low load)

Case 3: Generator ON (high load)

Case 4: Generator OFF

## Simulation
Simulations performed in python using pandapower
https://www.pandapower.org/start/

### Design Simplifications and Assumptions
* Constant power loads (PQ)
* Typical line imepedance values
* Balanced 3-phase system
* Harmonics are ignored
