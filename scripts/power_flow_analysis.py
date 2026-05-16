"""
MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
Aashna Sharma, May 2026

Power flow analysis
"""
import pandapower as pp
from power_flow_network import PowerFlowNetwork
from pandapower import shortcircuit


def run_case(name, gen_power, reverse_power_check=True):
    # Setup network
    pfn = PowerFlowNetwork()
    gen = pfn.full_config_setup()
    pfn.print_network_details()
    pfn.plot_network()
    pfn.net.sgen.at[gen, "p_mw"] = gen_power

    # Run simulation
    pp.runpp(
        pfn.net,
        algorithm="nr",     # Newton-Raphson
        max_iteration=30,
    )

    # Print summary
    pfn.print_power_flow_summary(name)

    if reverse_power_check:
        # Reverse power check
        pfn.reverse_power_check()

    # return {
    #     "voltages": pfn.net.res_bus.vm_pu.copy(),
    #     "angles": pfn.net.res_bus.va_degree.copy()
    # }
    return pfn


def power_flow_generator_off(name="CASE 1: Generator OFF"):
    pfn = run_case(name=name, gen_power=0.0)


def power_flow_generator_variable(name="CASE 2: Generator 30%", gen_power=0.03):
    pfn = run_case(name=name, gen_power=gen_power)
    

def power_flow_generator_full(name="CASE 4: Generator ON (100%)"):
    pfn = run_case(name=name, gen_power=0.1)
    pfn.plot_voltage(title=f"Bus Voltage Profile | {name}")


def short_circuit_analysis():
    """
    Calculates minimal or maximal symmetrical short-circuit currents.
    The calculation is based on the method of the equivalent voltage source according to DIN/IEC EN 60909
    https://pandapower.readthedocs.io/en/latest/shortcircuit/run.html
    """
    pfn_sc = PowerFlowNetwork()
    pfn_sc.full_config_setup()
    print("\nRunning short circuit study...")
    shortcircuit.calc_sc(pfn_sc.net)
    print("\nShort Circuit Results")
    print(pfn_sc.net.res_bus_sc[["ikss_ka"]])

    # TODO: DG OFF vs ON fault current




if __name__ == "__main__":
    power_flow_generator_off()
    power_flow_generator_variable(name="CASE 2: Generator 30%", gen_power=0.03)
    power_flow_generator_variable(name="CASE 3: Generator 60%", gen_power=0.06)
    power_flow_generator_full()
    short_circuit_analysis()
