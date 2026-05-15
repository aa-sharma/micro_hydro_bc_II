"""
MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
Aashna Sharma, May 2026

Power flow analysis
"""
import pandapower as pp
from power_flow_network import PowerFlowNetwork
from pandapower import shortcircuit

def generator_off():
    pfn_OFF = PowerFlowNetwork()
    pfn_OFF.full_config_setup()
    pfn_OFF.print_network_details()
    pfn_OFF.net.sgen["in_service"] = False
    pp.runpp(
        pfn_OFF.net,
        algorithm="nr",     # Newton-Raphson
        init="flat",
        max_iteration=30,
        enforce_q_lims=True
    )
    pfn_OFF.print_output_summary()
    pfn_OFF.plot_voltage(title="Bus Voltage Profile (Generator OFF)")
    pp.plotting.simple_plot(pfn_OFF.net)


def generator_on():
    pfn_ON = PowerFlowNetwork()
    pfn_ON.full_config_setup()
    pfn_ON.print_network_details()
    pfn_ON.net.sgen["in_service"] = True
    pp.runpp(
        pfn_ON.net,
        algorithm="nr",     # Newton-Raphson
        init="flat",
        max_iteration=30,
        enforce_q_lims=True
    )
    pfn_ON.print_output_summary()
    pfn_ON.plot_voltage(title="Bus Voltage Profile (Generator ON)")


def generator_sensitivity():
    # Generator Sensitivity Analysis
    # Vary output
    # TODO: plot Bus 4 voltage vs generation
    pfn_gen = PowerFlowNetwork()
    pfn_gen.full_config_setup()
    outputs = [0, 0.03, 0.06, 0.1]
    results = []
    for p in outputs:
        pfn_gen.net.sgen.at[0, "p_mw"] = p
        pp.runpp(pfn_gen.net)
        results.append(pfn_gen.net.res_bus.vm_pu.copy())
    print(results)

def reverse_power_flow_check():
    # transformer loading:
    pfn_rv = PowerFlowNetwork()
    pfn_rv.full_config_setup()
    pfn_rv.res_trafo.loading_percent()

def short_circuit_analysis():
    """
    Calculates minimal or maximal symmetrical short-circuit currents.
    The calculation is based on the method of the equivalent voltage source according to DIN/IEC EN 60909
    https://pandapower.readthedocs.io/en/latest/shortcircuit/run.html
    """
    pfn_sc = PowerFlowNetwork()
    pfn_sc.full_config_setup()
    shortcircuit.calc_sc(pfn_sc.net, fault='3ph')
    # TODO: DG OFF vs ON fault current




if __name__ == "__main__":
    generator_off()
    # generator_on()
    # generator_sensitivity()
    # reverse_power_flow_check()
    # short_circuit_analysis()
