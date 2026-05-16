"""
MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
Aashna Sharma, May 2026

Power flow analysis
"""
import pandapower as pp
from power_flow_network import PowerFlowNetwork
from pandapower import shortcircuit
import psse_plot

def run_case(name, gen_power, reverse_power_check=True):
    # Setup network
    pfn = PowerFlowNetwork()
    gen = pfn.full_config_setup()
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
    results = {
        "voltages": pfn.net.res_bus.vm_pu.copy(),
        "angles": pfn.net.res_bus.va_degree.copy()
    }
    return pfn, results


def power_flow_generator_off(name="CASE 1: Generator OFF", plot=True):
    """Perform power flow analysis while generator is OFF"""
    pfn, results = run_case(name=name, gen_power=0.0)
    if plot:
        psse_plot.plot_voltage_profiles(results=results, case=name)
        psse_plot.plot_voltage_angles(results=results, case=name)
        psse_plot.plot_line_loading(net=pfn.net, case=name)
        psse_plot.plot_transformer_loading(net=pfn.net, case=name)
    return pfn, results

def power_flow_generator_variable(name="CASE 2: Generator 30%", gen_power=0.03, plot=True):
    """Perform power flow analysis while generator is operating at x% capacity"""
    pfn, results = run_case(name=name, gen_power=gen_power)
    if plot:
        psse_plot.plot_voltage_profiles(results=results, case=name)
        psse_plot.plot_voltage_angles(results=results, case=name)
        psse_plot.plot_line_loading(net=pfn.net, case=name)
        psse_plot.plot_transformer_loading(net=pfn.net, case=name)
    return pfn, results

def power_flow_generator_full(name="CASE 4: Generator ON (100%)", plot=True):
    """Perform power flow analysis while generator is operating at full capacity"""
    pfn, results = run_case(name=name, gen_power=0.1)
    if plot:
        psse_plot.plot_voltage_profiles(results=results, case=name)
        psse_plot.plot_voltage_angles(results=results, case=name)
        psse_plot.plot_line_loading(net=pfn.net, case=name)
        psse_plot.plot_transformer_loading(net=pfn.net, case=name)
    return pfn, results


def sweep_generator():
    """Perform power flow analysis sweeping through [0, 0.03, 0.06, 0.1] generator operating conditions"""
    pass


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
    psse_plot.plot_short_circuit(net=pfn_sc.net)


def config_network_details():
    pfn = PowerFlowNetwork()
    pfn.full_config_setup()
    pfn.print_network_details()
    psse_plot.plot_network(net=pfn.net)



if __name__ == "__main__":
    config_network_details()
    power_flow_generator_off()
    # power_flow_generator_variable(name="CASE 2: Generator 30%", gen_power=0.03)
    # power_flow_generator_variable(name="CASE 3: Generator 60%", gen_power=0.06)
    # power_flow_generator_full()
    # short_circuit_analysis()
