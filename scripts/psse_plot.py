import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandapower as pp


def plot_network(net):
    """Plot network
    https://pandapower.readthedocs.io/en/latest/plotting/matplotlib/simple_plot.html"""
    pp.plotting.simple_plot(net,
                            line_width=2,
                            bus_size=2,
                            ext_grid_size=5,
                            trafo_size=2,
                            plot_loads=True,
                            plot_gens=True,
                            plot_sgens=True,
                            load_size=1,
                            gen_size=2,
                            sgen_size=5)

plt.rcParams.update({
    "figure.figsize": (10, 6),
    "font.size": 11,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.4,
    "axes.linewidth": 1.2,
    "lines.linewidth": 2.2,
    "lines.markersize": 7,
    "legend.frameon": True,
    "legend.framealpha": 1.0,
    "savefig.dpi": 300
})


def plot_voltage_profiles(results, case):
    """Plot Voltage Profiles"""
    plt.figure()
    plt.plot(
        results["voltages"].values,
        marker='o',
        label="Case"
    )
    plt.axhline(1.05, color='red', linestyle='--', label='Upper Limit')
    plt.axhline(0.95, color='red', linestyle='--', label='Lower Limit')
    plt.title(f"Bus Voltage Profile | {case}")
    plt.xlabel("Bus Number")
    plt.ylabel("Voltage (p.u.)")
    plt.xticks(range(len(results["voltages"])))
    plt.ylim(0.999000, 1.0001)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_voltage_angles(results, case):
    plt.figure()
    plt.plot(
        results["angles"].values,
        marker='s',
        label="Case"
    )
    plt.title(f"Voltage Angle Profile | {case}")
    plt.xlabel("Bus Number")
    plt.ylabel("Angle (degrees)")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_line_loading(net, case):
    plt.figure()
    loading = net.res_line["loading_percent"]
    plt.bar(
        range(len(loading)),
        loading
    )
    plt.axhline(100, linestyle='--', color='red', label='Thermal Limit')
    plt.title(f"Line Loading | {case}")
    plt.xlabel("Line")
    plt.ylabel("Loading (%)")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_transformer_loading(net, case):
    plt.figure()
    loading = net.res_trafo["loading_percent"]
    plt.bar(
        range(len(loading)),
        loading
    )
    plt.axhline(100, linestyle='--', color='red', label='Rated Limit')
    plt.title(f"Transformer Loading | {case}")
    plt.xlabel("Transformer")
    plt.ylabel("Loading (%)")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_short_circuit(net, case):
    plt.figure()
    sc_vals = net.res_bus_sc["ikss_ka"]
    plt.bar(range(len(sc_vals)), sc_vals)
    plt.title(f"Short Circuit Current | {case}")
    plt.xlabel("Bus")
    plt.ylabel("Fault Current (kA)")
    plt.tight_layout()
    plt.show()