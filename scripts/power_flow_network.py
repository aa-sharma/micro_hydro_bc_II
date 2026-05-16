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
                    [Bus 3] -- (Transformer 0.48kV / 12.47kV) -- (Micro-hydro 100 kW)
        """
        # Initialize network
        # reference apparent power for per unit system (sn_mva) = 1.0, frequency (f) = 60Hz
        self.net = pp.create_empty_network(name="microhydro_southwest_BC", sn_mva=1.0, f_hz=60)

        # Bus
        self.bus_slack = pp.create_bus(self.net, vn_kv=12.47, name="Slack Bus")
        self.bus_1 = pp.create_bus(self.net, vn_kv=12.47, name="Load Bus 1")
        self.bus_2 = pp.create_bus(self.net, vn_kv=12.47, name="Load Bus 2")
        self.bus_3 = pp.create_bus(self.net, vn_kv=12.47, name="Load Bus 3")
        self.bus_lv = pp.create_bus(self.net, vn_kv=0.48, name="Hydro Generator LV")

        # Slack (grid)
        pp.create_ext_grid(
            self.net,
            self.bus_slack,
            vm_pu=1.0,              # voltage at slack node
            va_degree=0,            # voltage angle at the slack node in degrees
            s_sc_max_mva=500,       # maximal short circuit apparent power
            rx_max=0.1,             # maximal R/X-ratio
            name="BC Hydro Grid"
        )

        # Distribution Lines
        pp.create_line_from_parameters(self.net, self.bus_slack, self.bus_1, 1.0,
                                       R_OHM_PER_KM, X_OHM_PER_KM, C_NF_PER_KM, MAX_I_KA)
        pp.create_line_from_parameters(self.net, self.bus_1, self.bus_2, 1.0,
                                       R_OHM_PER_KM, X_OHM_PER_KM, C_NF_PER_KM, MAX_I_KA)
        pp.create_line_from_parameters(self.net, self.bus_2, self.bus_3, 1.0,
                                       R_OHM_PER_KM, X_OHM_PER_KM, C_NF_PER_KM, MAX_I_KA)

        # Loads
        pp.create_load(self.net, self.bus_1, p_mw=0.04, q_mvar=0.015, name="Load 1")
        pp.create_load(self.net, self.bus_2, p_mw=0.03, q_mvar=0.01, name="Load 2")
        pp.create_load(self.net, self.bus_3, p_mw=0.05, q_mvar=0.02, name="Load3")

        # Transformer (Step-up)
        # 0.48kV -> 12.47kV
        pp.create_transformer_from_parameters(
            self.net,
            hv_bus=self.bus_3,              # bus on the high-voltage side
            lv_bus=self.bus_lv,             # bus on the low-voltage side
            sn_mva=0.15,                    # rated apparent power
            vn_hv_kv=12.47,                 # rated voltage on high voltage side
            vn_lv_kv=0.48,                  # rated voltage on low voltage side
            vk_percent=6,                   # relative short-circuit voltage
            vkr_percent=1.2,                # real part of relative short-circuit voltage
            pfe_kw=0.5,                     # iron losses in kW
            i0_percent=0.1,                 # open loop losses in percent of rated current
            shift_degree=0,                 # angle shift over the transformer
            name="Hydro Step-Up Transformer"
        )

        # 100kW Micro-hydro generator
        gen = pp.create_sgen(
            self.net,
            self.bus_lv,
            p_mw=0.1,                      # real power of the generator
            q_mvar=-0.02,                  # reactive power of the sgen
            name="Micro-Hydro 100kW Generator"
        )

        return gen

    def print_network_details(self):
        print(f"System Details")
        print(f"========Bus========\n{self.net.bus}\n")
        print(f"========Ext. Grid========\n{self.net.ext_grid}\n")
        print(f"========Line========\n{self.net.line}\n")
        print(f"========Transformer========\n{self.net.trafo}\n")
        print(f"========Load========\n{self.net.load}\n")
        print(f"========Generator========\n{self.net.sgen}\n")

    def print_power_flow_summary(self, name):
        print("\n" + "=" * 60)
        print(name)
        print("=" * 60)
        print("\nBus Voltages")
        print(self.net.res_bus[["vm_pu", "va_degree"]])
        print("\nLine Loading")
        print(self.net.res_line[["loading_percent", "p_from_mw"]])
        print("\nTransformer")
        print(self.net.res_trafo[["loading_percent", "p_hv_mw", "p_lv_mw"]])

    def reverse_power_check(self):
        """
        Interpretation:
        positive = importing from grid
        negative = exporting to grid
        If generation > local load, reverse power occurs.
        """
        p_to_grid = self.net.res_ext_grid["p_mw"].iloc[0]
        print(f"\nGrid import (+) / export (-): {p_to_grid:.4f} MW")
        if p_to_grid < 0:
            print("Reverse power flow detected")
        else:
            print("No reverse power flow detected ")
