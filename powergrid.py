import numpy as np
import math
import pandapower as pp
import pandapower.networks as pn
import pandapower.shortcircuit as sc
import pandapower.plotting as plot
from soltrade import db
from soltrade.models import User, Group

# function to calculate Euclidean distance between two points 
def calc_distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

# function to create the power network
def create_net():
    users = User.query.all()
    net = pp.create_empty_network()
    # first bar — connecting to external grid
    bar1 = pp.create_bus(net, name="HV Busbar 0", vn_kv=110, type="b", geodata=(40, 5))
    pp.create_ext_grid(net, bar1, vm_pu=1.02, va_degree=50)
    # second bar — to connect to residential loads and transformer
    bar2_loc = (40, 10)
    bar2 = pp.create_bus(net, name="HV Busbar 1", vn_kv=20, type="b", geodata=bar2_loc)
    # transformer, connected to 
    trafo1 = pp.create_transformer(net, bar1, bar2, name="110kV/20kV transformer", std_type="25 MVA 110/20 kV")
    for i, user in enumerate(users):
        geodata = (int(str(user.loc)[:2]), int(str(user.loc)[2:4]))
        bus = pp.create_bus(net, name="Load Bus" + str(i), vn_kv=10, geodata=geodata, type="b")
        load = pp.create_load(net, bus, p_mw=1, q_mvar=0.5, scaling=0.6, name="load")
        length_km = (calc_distance(bar2_loc, geodata)) * .01
        line = pp.create_line(net, from_bus=bus, to_bus=bar2, length_km=length_km, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line" + str(i))
    return net


# function to check validity of transaction between users 
# returns True if transaction is valid, False otherwise
def check_transaction(power, user):
    # must convert kW to MW — these functions take in MW, transactions are in kW
    # pp.create_sgen(net, bus, p_mw=transaction, q_mvar=0)
    net = create_net()
    pp.runpp(net)
    print(net.res_line.loading_percent)
    plot.simple_plot(net, show_plot=True)
    return True

check_transaction(10, "placeholder")

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