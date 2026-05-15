"""
MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
Aashna Sharma, May 2026

Power flow analysis
"""
import pandapower as pp
from power_flow_network import PowerFlowNetwork

# CASE 1: Generator OFF
pfn_OFF = PowerFlowNetwork()
pfn_OFF.full_config_setup()
pfn_OFF.print_network_details()
pfn_OFF.net.sgen["in_service"] = False
pp.runpp(
    pfn_OFF.net,
    algorithm="nr",
    init="flat",
    max_iteration=30,
    enforce_q_lims=True
)
pfn_OFF.print_output_summary()








