"""
MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
Aashna Sharma
May 2026
"""
import pandapower as pp

VN_KV = 12.47
R_OHM_PER_KM = 0.40
X_OHM_PER_KM = 0.30
C_NF_PER_KM = 10
MAX_I_KA = 0.20
VM_PU = 1.02

class PowerFlowNetwork:
    def __init__(self, net=None, vn_kv=VN_KV):
        self.net = net
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








