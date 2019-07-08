import numpy as np
import math
import pandapower as pp
import pandapower.networks as pn
import pandapower.shortcircuit as sc
import pandapower.plotting as plot
from soltrade.models import User

# class to model the electricity flow of a residential power grid
class PowerGrid:
    # initialization, constructor
    def __init__(self):
        self._net = pp.create_empty_network()
        # first bar — connecting to external grid
        bar1 = pp.create_bus(self._net, name="HV Busbar 0", vn_kv=110, type="b", geodata=(40, 5))
        pp.create_ext_grid(self._net, bar1, vm_pu=1.02, va_degree=50)
        # second bar — to connect to residential loads and transformer
        self._bar2_loc = (40, 10)
        self._bar2 = pp.create_bus(self._net, name="HV Busbar 1", vn_kv=20, type="b", geodata=self._bar2_loc)
        # transformer, connected to first bar
        trafo1 = pp.create_transformer(self._net, bar1, self._bar2, name="110kV/20kV transformer", std_type="25 MVA 110/20 kV")
        self._bus_num = 1
    
    # add prosumer to the power grid
    def add_user(self, username):
        self._bus_num += 1
        user = User.query.filter_by(username=username).first()
        user.bus = self._bus_num
        # getting user location
        geodata = (int(str(user.loc)[:2]), int(str(user.loc)[2:4]))
        print(geodata)
        # creating bus for user
        bus = pp.create_bus(self._net, name="Bus" + str(self._bus_num), vn_kv=10, geodata=geodata, type="b")
        # creating load for user
        load = pp.create_load(self._net, bus, p_mw=1, q_mvar=0.5, scaling=0.6, name="load")
        length_km = (self.calc_distance(self._bar2_loc, geodata)) * .01
        line = pp.create_line(self._net, from_bus=bus, to_bus=self._bar2, length_km=length_km, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line" + str(self._bus_num))

    # function to check validity of transaction between users 
    # returns True if transaction is valid, False otherwise
    def check_transaction(self, power, username):
        user = User.query.filter_by(username=username).first()
        # must convert kW to MW — these functions take in MW, transactions are in kW
        pp.create_sgen(self._net, user.bus, p_mw=power, q_mvar=0)
        pp.runpp(self._net)
        violate = violations(net)
        print(violate)
        return violate[0]

    # method used to determine whether loading capacity is being violated
    def violations(self, net):
        pp.runpp(net)
        if net.res_line.loading_percent.max() > 50:
            return (True, "Line \n Overloading")
        elif net.res_trafo.loading_percent.max() > 50:
            return (True, "Transformer \n Overloading")
        elif net.res_bus.vm_pu.max() > 1.04:
            return (True, "Voltage \n Violation")
        else:
            return (False, None)
    
    # method to plot the grid graphically
    def plot_grid(self):
        plot.simple_plot(self._net, show_plot=True)
    
    # helper function to calculate Euclidean distance between two points 
    def calc_distance(self, p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)