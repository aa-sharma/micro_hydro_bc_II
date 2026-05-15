"""
MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
Aashna Sharma
May 2026
"""
import pandapower as pp

net = pp.create_empty_network()

# ============================== SETUP ==============================
vn_kv = 12.47

# Bus
bus0 = pp.create_bus(net, vn_kv=vn_kv, name="Slack Bus")
bus1 = pp.create_bus(net, vn_kv=vn_kv, name="Bus 1")
bus2 = pp.create_bus(net, vn_kv=vn_kv, name="Bus 2")
bus3 = pp.create_bus(net, vn_kv=vn_kv, name="Bus 3 (DG)")
bus4 = pp.create_bus(net, vn_kv=vn_kv, name="Bus 4")


# Slack (grid)
pp.create_ext_grid(net, bus0, vm_pu=1.02, va_degree=0)

# Distribution Lines
pp.create_line_from_parameters(
    net, bus0, bus1, 1.0,
    r_ohm_per_km=0.40,
    x_ohm_per_km=0.30,
    c_nf_per_km=10,
    max_i_ka=0.2
)
pp.create_line_from_parameters(net, bus1, bus2, 1.0, 0.40, 0.30, 10, 0.2)
pp.create_line_from_parameters(net, bus2, bus3, 1.0, 0.40, 0.30, 10, 0.2)
pp.create_line_from_parameters(net, bus3, bus4, 1.0, 0.40, 0.30, 10, 0.2)


# Loads
pp.create_load(net, bus2, p_mw=0.04, q_mvar=0.015)
pp.create_load(net, bus3, p_mw=0.03, q_mvar=0.01)
pp.create_load(net, bus4, p_mw=0.05, q_mvar=0.02)


# 100kW Micro-hydro generator
pp.create_sgen(
    net,
    bus3,
    p_mw=0.1,
    q_mvar=0.0,
    min_q_mvar=-0.05,
    max_q_mvar=0.05,
    name="Micro-Hydro 100kW Generator"
)

print(f"System Details")
print(f"========Bus========\n{net.bus}\n")
print(f"========Ext. Grid========\n{net.ext_grid}\n")
print(f"========Line========\n{net.line}\n")
print(f"========Transformer========\n{net.trafo}\n")
print(f"========Load========\n{net.load}\n")
print(f"========Generator========\n{net.sgen}\n")

# ============================== CASES ==============================

# CASE 1: Generator OFF
net.sgen["in_service"] = False
pp.runpp(
    net,
    algorithm="nr",
    init="flat",
    max_iteration=30,
    enforce_q_lims=True
)

print(f"Bus voltages\n{net.res_bus.vm_pu}")
print(f"Line Loading\n{net.res_line.loading_percent}")
print(f"Transformer\n{net.res_trafo.loading_percent}")