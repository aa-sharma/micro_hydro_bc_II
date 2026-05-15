"""
MICRO-HYDROPOWER DESIGN PART II - GRID INTEGRATION & POWER SYSTEM MODELLING
Aashna Sharma
May 2026
"""
import pandapower as pp

net = pp.create_empty_network()

# ============================== SETUP ==============================
# Slack / grid side
bus_slack = pp.create_bus(net, vn_kv=25, name="Slack Bus")

# Transformer LV side
bus_lv = pp.create_bus(net, vn_kv=0.4, name="LV Bus")

# Feeder buses
bus2 = pp.create_bus(net, vn_kv=0.4, name="Bus 2")
bus3 = pp.create_bus(net, vn_kv=0.4, name="Bus 3")
bus4 = pp.create_bus(net, vn_kv=0.4, name="Bus 4")
bus5 = pp.create_bus(net, vn_kv=0.4, name="Bus 5 (DG bus)")

# Transformer
# pp.create_transformer_from_parameters(
#     net,
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

    # hv_bus=bus_slack,
    # lv_bus=bus_lv,

pp.create_transformer_from_parameters(
    net,
    hv_bus=0,
    lv_bus=1,
    sn_mva=0.5,
    vn_hv_kv=25,
    vn_lv_kv=0.4,
    vk_percent=6,   # DO NOT set too low (this matters)
    vkr_percent=1.0,
    pfe_kw=0.5,
    i0_percent=0.1
)

# Radial feeder
line_params = {
    "length_km": 1.0,
    "std_type": "NAYY 4x150 SE"
}

pp.create_line(net, bus_lv, bus2, **line_params)
pp.create_line(net, bus2, bus3, **line_params)
pp.create_line(net, bus3, bus4, **line_params)
pp.create_line(net, bus4, bus5, **line_params)

# Loads
pp.create_load(net, bus2, p_mw=0.03, q_mvar=0.015)
pp.create_load(net, bus3, p_mw=0.04, q_mvar=0.02)
pp.create_load(net, bus4, p_mw=0.02, q_mvar=0.01)
pp.create_load(net, bus5, p_mw=0.01, q_mvar=0.005)

# Grid (slack)
pp.create_ext_grid(net, bus_slack, vm_pu=1.02)
net.ext_grid.loc[0, "vm_pu"] = 1.02
net.ext_grid.loc[0, "va_degree"] = 0

# Micro-Hydro Generator
pp.create_sgen(
    net,
    bus5,
    p_mw=0.1,   # 100 kW
    q_mvar=0.0,
    name="Micro Hydro 100kW"
)



# ============================== CASES ==============================
# Generator OFF
net.sgen["in_service"] = False
print(f"System Details")
print(f"========Bus========\n{net.bus}")
print(f"========Ext. Grid========\n{net.ext_grid}")
print(f"========Line========\n{net.line}")
print(f"========Transformer========\n{net.trafo}")
print(f"========Load========\n{net.load}")
print(f"========Generator========\n{net.sgen}")

pp.runpp(
    net,
    algorithm="gs",   # Gauss-Seidel (more stable, slower)
    max_iteration=50
)
print(net.res_bus.vm_pu)
print(net.res_line.loading_percent)
print(net.res_trafo.loading_percent)