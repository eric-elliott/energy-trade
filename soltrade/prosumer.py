import numpy as np
from random import uniform
from random import randint

# this class models a prosumer, keeping track of current device decisions, energy
# generated, money, etc.
class Prosumer:
    
    def __init__(self, name, p_internal, decisions, p_renewable, panels, e_bid):
        self._name = name
        # environment vars
        self._p_internal = p_internal 
        # temp, water heater, laundry, lighting, fridge, oven
        self._devices = np.asarray([.49, .15, .14, .13, .05, .04])
        # 30 is avg. kW of energy used per home
        self._avg_energy_day = 30
        self._demand = np.sum(np.multiply(np.asarray(self._devices), np.asarray(decisions))) * self._avg_energy_day
        self._p_renewable = p_renewable
        # action vars
        self._decisions = decisions
        self._e_bid =  e_bid
        # excess energy for the day
        self._excess = 0
        # money, in dollars
        self._daily_money = 200.0
        self._total_money = 5000.0
        self._money_spent = 0.0
        self._e_money_earned = 0.0
        self._prev_costs = []
        self._cur_cost = 0.0
        # number of solar panels prosumer owns 
        self._panels = panels
        # maybe allow prosumer to have battery for energy storage?

    # updating renewable energy produced
    def update_renewable_energy(self):
        self._p_renewable = uniform(.90, 1.05) * self._panels

    # updating the energy demand -- using device decisions to determine this
    def update_energy_demand(self):
        self._demand = np.sum(np.multiply(np.asarray(self._devices), np.asarray(self._decisions))) * self._avg_energy_day
    
    # updating the current excess energy
    def update_excess_energy(self):
        # excess energy could be stored in battery -- maybe (+=)
        self._excess = self._p_renewable - self._demand
    
    # updating the total money earned 
    def update_money_earned(self):
        self._total_money += self._daily_money

    # updating decisions of whether to turn on or off devices -- should be reworked and optimized, random currently
    def update_device_decisions(self):
        if len(self._prev_costs) > 0 and self._prev_costs[-1] < self._cur_cost:
            self.switch_single_device(1, 1)
        else:
            self.switch_single_device(0, 1)
        # print(self._name)
        # print(self._prev_cost)
        # print(self._cur_cost)
        # print(self._decisions)
        # print()

    def switch_single_device(self, flip, amount):
        count = 0
        for i in range(0, len(self._decisions)):
            if self._decisions[i] != flip:
                self._decisions[i] = flip
                count += 1
            if count >= amount:
                break