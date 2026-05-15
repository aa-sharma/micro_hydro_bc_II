### MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
> This projects build on [Part I - Site Assessment](https://github.com/aa-sharma/micro_hydro_bc) where we identified candidate locations for a micro-hydropower site in rural Southwest British Columbia. In this project, we assume a capacity of 100kW for the candidate site and conduct a distribution feeder impact study through load flow, voltage rise analysis, and reverse power flow check analysis.

## System
Micro-hydro → LV generator → transformer → distribution feeder → substation (grid)

## Areas of Study
1. Power flow (Voltage impact study)
2. Reverse power flow
3. Transformer behaviour
4. Short-circuit analysis

# Power Flow
Modelling a simple radial feeder:
Grid → 1 line → load → microhydro at midpoint or end

Case 1: No generation (normal load flow)

Case 2: Generator ON (low load)

Case 3: Generator ON (high load)

Case 4: Generator OFF

# Parameters & Assumptions
Generator:
* 100 kW (0.1 MW)
* 0.48 kV
* synchronous generator (modeled as controlled injection)

Transformer
* 0.48 / 12.47 kV
* 0.25 MVA rating
* typical distribution impedance

Line
* 5 km 12.47 kV overhead feeder
* typical R/X values for distribution

Load
* 80 kW + 30 kVAR (residential/light commercial)

Grid
* infinite bus (slack)

# Simulation
Simulations performed in python using pandapower
https://www.pandapower.org/start/
