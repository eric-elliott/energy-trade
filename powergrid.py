import numpy as np
import random
import pandapower as pp
import pandapower.networks as pn
import pandapower.shortcircuit as sc
import pandapower.plotting as plot
from soltrade import db
from soltrade.models import User, Group

# getting number of users in simulation
num_users = db.session.query(User).count()
net = pp.create_empty_network()

x = random.randint(5 , 35)
y = random.randint(5, 35)
geod = (x, y)
geod2 = (x + 3, y - 4)
user_buses = []
user_loads = []
user_lines = []
bar1 = pp.create_bus(net, name="HV Busbar 0", vn_kv=110, type="b", geodata=geod)
pp.create_ext_grid(net, bar1, vm_pu=1.02, va_degree=50)
bar2 = pp.create_bus(net, name="HV Busbar 1", vn_kv=20, type="b", geodata=geod2)
trafo1 = pp.create_transformer(net, bar1, bar2, name="110kV/20kV transformer", std_type="25 MVA 110/20 kV")

# creating loads, buses, lines
prev_bus = None
for i in range(num_users + 1):
    # making coordinates better
    x = random.randint(2 , 30)
    y = random.randint(2, 30)
    geod = (x, y)
    if i != num_users:
        bus = pp.create_bus(net, name="Load Bus" + str(i), vn_kv=10, geodata=geod, type="b")
        if bool(random.getrandbits(1)):
            solargen = pp.create_sgen(net, bus, p_mw=1, q_mvar=0)
    load = pp.create_load(net, bus, p_mw=2, q_mvar=4, scaling=0.6, name="load")
    if i == 0:
        line = pp.create_line(net, from_bus=bar2, to_bus=bus, length_km=2.5, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line" + str(i))
    elif i == num_users:
        line = pp.create_line(net, from_bus=prev_bus, to_bus=bar2, length_km=2.5, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line" + str(i))
    else:
        line = pp.create_line(net, from_bus=prev_bus, to_bus=bus, length_km=2.5, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line" + str(i))
    user_buses.append(bus)
    user_lines.append(line)
    user_loads.append(load)
    prev_bus = bus
    print(prev_bus)

pp.runpp(net)
print(net.res_line.loading_percent)
plot.simple_plot(net, show_plot=True)




# method used to determine whether loading capacity is being violated
def violations(net):
    pp.runpp(net)
    if net.res_line.loading_percent.max() > 50:
        return (True, "Line \n Overloading")
    elif net.res_trafo.loading_percent.max() > 50:
        return (True, "Transformer \n Overloading")
    elif net.res_bus.vm_pu.max() > 1.04:
        return (True, "Voltage \n Violation")
    else:
        return (False, None)