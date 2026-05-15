"""
MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
Aashna Sharma, May 2026

Network Definition
"""

import pandapower as pp
import matplotlib.pyplot as plt


VN_KV = 12.47
R_OHM_PER_KM = 0.40
X_OHM_PER_KM = 0.30
C_NF_PER_KM = 10
MAX_I_KA = 0.20
VM_PU = 1.02


class PowerFlowNetwork:
    def __init__(self, vn_kv=VN_KV):
        self.vn_kv = vn_kv

    def full_config_setup(self):
        """Fully setup the below configuration
                [GRID SLACK (12.47 kV)]
                        |
                    [Bus 1]
                        |
                    [Bus 2]
                        |
                    [Bus 3] ---- (Micro-hydro 100 kW)
                        |
                    [Bus 4]
        """
        self.net = pp.create_empty_network()

        # Bus
        self.bus0 = pp.create_bus(self.net, vn_kv=VN_KV, name="Slack Bus")
        self.bus1 = pp.create_bus(self.net, vn_kv=VN_KV, name="Bus 1")
        self.bus2 = pp.create_bus(self.net, vn_kv=VN_KV, name="Bus 2")
        self.bus3 = pp.create_bus(self.net, vn_kv=VN_KV, name="Bus 3 (DG)")
        self.bus4 = pp.create_bus(self.net, vn_kv=VN_KV, name="Bus 4")
                
        # Slack (grid)
        pp.create_ext_grid(self.net, self.bus0, vm_pu=VM_PU, va_degree=0)

        # Distribution Lines
        pp.create_line_from_parameters(self.net, self.bus0, self.bus1, 1.0,
                                       R_OHM_PER_KM, X_OHM_PER_KM, C_NF_PER_KM, MAX_I_KA)
        pp.create_line_from_parameters(self.net, self.bus1, self.bus2, 1.0,
                                       R_OHM_PER_KM, X_OHM_PER_KM, C_NF_PER_KM, MAX_I_KA)
        pp.create_line_from_parameters(self.net, self.bus2, self.bus3, 1.0,
                                       R_OHM_PER_KM, X_OHM_PER_KM, C_NF_PER_KM, MAX_I_KA)
        pp.create_line_from_parameters(self.net, self.bus3, self.bus4, 1.0,
                                       R_OHM_PER_KM, X_OHM_PER_KM, C_NF_PER_KM, MAX_I_KA)

        # Transformer
        # pp.create_transformer_from_parameters(
        #     self.net,
        #     hv_bus=bus_slack,
        #     lv_bus=bus_lv,
        #     sn_mva=0.5,
        #     vn_hv_kv=25,
        #     vn_lv_kv=0.4,
        #     vkr_percent=1.0,
        #     vk_percent=6.0,
        #     pfe_kw=0.5,
        #     i0_percent=0.1,
        #     name="25kV/400V Transformer"
        # )

        # Loads
        pp.create_load(self.net, self.bus2, p_mw=0.04, q_mvar=0.015)
        pp.create_load(self.net, self.bus3, p_mw=0.03, q_mvar=0.01)
        pp.create_load(self.net, self.bus4, p_mw=0.05, q_mvar=0.02)

        # 100kW Micro-hydro generator
        pp.create_sgen(
            self.net,
            self.bus3,
            p_mw=0.1,
            q_mvar=0.0,
            min_q_mvar=-0.05,
            max_q_mvar=0.05,
            name="Micro-Hydro 100kW Generator"
        )

    def print_network_details(self):
        print(f"System Details")
        print(f"========Bus========\n{self.net.bus}\n")
        print(f"========Ext. Grid========\n{self.net.ext_grid}\n")
        print(f"========Line========\n{self.net.line}\n")
        print(f"========Transformer========\n{self.net.trafo}\n")
        print(f"========Load========\n{self.net.load}\n")
        print(f"========Generator========\n{self.net.sgen}\n")

    def print_output_summary(self):
        print(f"Bus voltages\n{self.net.res_bus.vm_pu}")
        print(f"Line Loading\n{self.net.res_line.loading_percent}")
        print(f"Transformer\n{self.net.res_trafo.loading_percent}")

    def plot_voltage(self,
                     title='Bus Voltage Profile',
                     xlabel='Bus Index',
                     ylabel='Voltage (p.u.)'):
        plt.plot(self.net.res_bus.vm_pu.values, marker='o')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid()
        plt.show()

    def plot_psse_style(self):
        plt.style.use('default')
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['axes.edgecolor'] = 'black'
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.color'] = '0.85'
        plt.rcParams['grid.linestyle'] = '-'
        plt.rcParams['font.size'] = 11

    def plot_voltage_profile(base,
                             dg_on,
                             bus_labels=["Slack", "Bus1", "Bus2", "Bus3", "Bus4"],
                             xlabel='Bus',
                             ylabel='Voltage (p.u.)',
                             title='Voltage Profile Comparison'):
        x = range(len(base))
        plt.figure(figsize=(8,4))
        plt.plot(x, base, label="No DG", linewidth=2)
        plt.plot(x, dg_on, label="100 kW DG", linewidth=2, linestyle="--")
        plt.axhline(1.05, color='r', linestyle=':', linewidth=1)
        plt.axhline(0.95, color='r', linestyle=':', linewidth=1)
        plt.xticks(x, bus_labels)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        plt.show()