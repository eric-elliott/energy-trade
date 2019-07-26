import numpy as np
import pandapower as pp
import pandapower.networks as pn
import pandapower.plotting as plot
from soltrade.models import User, Offer

"""
wrapper class to model the electricity flow of a residential power grid
"""
class PowerGrid:
    """
    initialization, constructor
    """
    def __init__(self):
        self._net = pn.create_kerber_vorstadtnetz_kabel_1()

    def check_energy(self, user_send, load_indices):
        print(user_send)
        for id1, send in user_send.items():
            violated, violation_type = self.violations(self._net)
            if violated:
                break
            else:
                bus_number = load_indices[id1]
                pp.create_sgen(self._net, bus_number, send/1000, q_mvar=1)
            return (violated, violation_type)
    
    """
    function to check validity of energy amount
    returns True if transaction is valid, False otherwise
    """
    # def check_offers(self, power, username):
    #     offers_by_least = Offer.query.order_by(desc(Offer.energy_offer))
    #     for offer in offers_by_least:
    #         violated, violation_type = violations(self._net)
    #         if violated:
    #             break
    #         else:
    #             bus_number = (2 * offer.user_id) + 1
    #             pp.create_sgen(self._net, bus_number, energy_offer, q_mvar=0)
    
    """
    method used to determine whether loading capacity is being violated
    """
    def violations(self, net):
        pp.runpp(net)
        # print(net.res_line.loading_percent.max())
        print(net.res_line.loading_percent.max())
        if net.res_line.loading_percent.max() > 50:
            return (True, "Line \n Overloading")
        elif net.res_trafo.loading_percent.max() > 50:
            return (True, "Transformer \n Overloading")
        elif net.res_bus.vm_pu.max() > 1.04:
            return (True, "Voltage \n Violation")
        else:
            return (False, None)
    
    """
    method to plot the grid graphically
    """
    def plot_grid(self):
        plot.simple_plot(self._net, show_plot=True)