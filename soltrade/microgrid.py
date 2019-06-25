from soltrade.prosumer import Prosumer
from soltrade.coordinator import Coordinator
from soltrade.retailer import Retailer
from random import uniform
import numpy as np

# this class models a microgrid, containing instances of prosumers, a coordinator,
# and a retailer
class MicroGrid:

    def __init__(self, num_prosumers, p_internal, p_external):
        # setting baseline price of energy -- this will stay constant
        self._baseline_p_internal = p_internal
        # setting value of p_internal -- this will fluctuate
        self._p_internal = p_internal
        # setting value of p_external -- this *might* fluctuate
        self._p_external = p_external
        self._num_prosumers = num_prosumers
        self._prosumers = self.initialize_prosumers()
        self._coordinator = Coordinator("Coordinator", p_external, e_bid = 0, p_internal = p_internal, e_exchange = 0)
        self._retailer = Retailer("Retailer", p_external * .75, p_external)
        # every hour? maybe day? -- day for now
        self._time = 0

    def initialize_prosumers(self):
        prosumers = [] 
        # list of names of prosumers, limits how many prosumers can exist in simulation
        self._names = ["alice", "bob", "charlie", "david", "ellie", "francis", "gene", \
            "hannah", "iago", "jenna", "karen", "lucas"]
        # if each of these are on 1, 0 otherwise
        decisions = np.asarray([1, 1, 1, 1, 1, 1])
        for i in range(self._num_prosumers):
            # number of solar panels here -- should be experimented with, currently semi-random
            panels = int(round(uniform(.9, 1.1) * 25))
            p_renewable = uniform(.90, 1.05) * panels
            p = Prosumer(self._names[i], self._p_internal, decisions, p_renewable, panels, e_bid = 0)
            prosumers.append(p)
        return prosumers

    def run_iterations(self, iterations):
        for i in range(self._time, self._time + iterations):
            # incrementing current time of the simulation
            self._time += 1

            # updating solar energy produced by each prosumer for the day
            self.update_all_renewable_energy()

            # updating energy demand from each prosumer over course of day
            self.update_all_energy_demand()

            # determining if there is an excess or lack of energy 
            self.update_all_excess_energy()

            # updating the money eanred for each prosumer
            self.update_all_money_earned()

            # prosumers now make their bids -- can probably improve this for better decision making
            self.update_all_bids()

            # updating decisions of what to leave on and off -- maybe place this after bidding? -- doing that
            self.update_all_device_decisions()

            # updating internal price for all agents now that transactions have taken place
            self.update_all_internal()
    
    # updating the money each prosumer has earned for the day
    def update_all_money_earned(self):
        for prosumer in self._prosumers:
            prosumer.update_money_earned()

    # updating the renewable energy generated for each prosumer
    def update_all_renewable_energy(self):
        for prosumer in self._prosumers:
            prosumer.update_renewable_energy()

    # updating the energy demand for each prosumer 
    def update_all_energy_demand(self):
        for prosumer in self._prosumers:
            prosumer.update_energy_demand()

    # updating the excess energy for each prosumer -- "excess" is a defecit of energy, when negative
    def update_all_excess_energy(self):
        for prosumer in self._prosumers:
            prosumer.update_excess_energy()

    # updating decisions for whether devices stay on
    def update_all_device_decisions(self):
        for prosumer in self._prosumers:
                prosumer.update_device_decisions()

    # updating bids of each prosumer, engaging in transaction -- can be further improved, "bidding" not really occurring currently
    def update_all_bids(self):
        excess = []
        # boolean list that keeps track of whether prosumer has lack of energy
        need_buy = [0] * self._num_prosumers
        # list that contains excess energy of prosumer -- 0 if no excess, or lack of energy
        can_sell = [0] * self._num_prosumers
        for prosumer in self._prosumers:
            excess.append(prosumer._excess)
        # sorting prosumers by "can sell" energy and "need to buy" energy
        for i, energy in enumerate(excess):
            if energy < 0:
                need_buy[i] = energy
            else:
                can_sell[i] = energy
        # adjusting the internal price based on how many people need energy
        buyers = sum(p < 0 for p in need_buy)
        # print(buyers)
        if buyers > 0:
            self._p_internal = (.8 * buyers) * self._p_internal
        else:
            self._p_internal = self._baseline_p_internal
        # now starting the "auction" process -- this can probably be further improved
        for i, energy in enumerate(need_buy):
            maximum_e = max(can_sell)
            # maybe change so excess energy can be bought? probably more realistic
            if (energy < 0 and maximum_e > energy) and (self._p_internal < self._p_external):
                max_ind = can_sell.index(maximum_e)
                can_sell[max_ind] -= abs(energy) 
                need_buy[i] = 0
                energy_cost = abs(self._p_internal * energy)
                # subtracting from prosumer who bought energy
                self._prosumers[i]._total_money -= energy_cost
                self._prosumers[i]._money_spent += energy_cost
                # adding money to prosumer purchased from
                self._prosumers[max_ind]._total_money += energy_cost
                self._prosumers[max_ind]._e_money_earned += energy_cost
                # setting previous costs to allow for better decision-making -- maybe use arrays?
                self._prosumers[i]._prev_cost = self._prosumers[i]._cur_cost
                self._prosumers[i]._cur_cost = energy_cost
            elif energy < 0:
                need_buy[i] = 0
                energy_cost = abs(self._p_external * energy)
                self._prosumers[i]._total_money -= energy_cost
                self._prosumers[i]._money_spent += energy_cost
                self._coordinator._e_exchange += abs(energy)
                # setting previous cost on purchase to allow for decision-making (again)
                self._prosumers[i]._prev_costs.append(self._prosumers[i]._cur_cost)
                self._prosumers[i]._cur_cost = energy_cost

    # updating the internal cost for the prosumers and coordinator
    def update_all_internal(self):
        for prosumer in self._prosumers:
            prosumer._p_internal = self._p_internal
        self._coordinator._p_internal = self._p_internal

    # updating the external cost for the coordinator and retailer
    def update_all_external(self):
       self._coordinator._p_external = self._p_external
       self._retailer._sell_for = self._p_external
    
    # printing stats for each prosumer
    def print_prosumer_stats(self):
        CSTART = '\033[94m'
        CEND = '\033[0m'
        for prosumer in self._prosumers:
            print(CSTART + str(prosumer._name) + CEND) 
            print("current excess energy: " + str(prosumer._excess))
            print("number of solar panels: " + str(prosumer._panels)) 
            print("current total money: " + str(prosumer._total_money))
            print("total money spent on energy: " + str(prosumer._money_spent))
            print("total money earned with energy: " + str(prosumer._e_money_earned))
    
    # printing stats for the coordinator
    def print_coordinator_stats(self):
        CSTART = '\033[94m'
        CEND = '\033[0m'
        print(CSTART + str(self._coordinator._name) + CEND)
        print("current internal price: " + str(self._coordinator._p_internal))
        print("total energy exchanged with retailer: " + str(self._coordinator._e_exchange))
    
    # printing stats for the retailer
    def print_retailer_stats(self):
        CSTART = '\033[94m'
        CEND = '\033[0m'
        print(CSTART + str(self._retailer._name) + CEND)
        print("currently buying energy for: " + str(self._retailer._buy_for))
        print("currently selling energy for: " + str(self._retailer._sell_for))