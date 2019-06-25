# * driver file to run REPL for interaction with simulation *

from prosumer import Prosumer
from coordinator import Coordinator
from microgrid import MicroGrid
from retailer import Retailer
import numpy as np
import sys
import time

CSTART1 = '\33[102m'
CSTART2 = '\33[91m'
CSTART3 = '\033[94m'
CEND = '\033[0m'

# starting REPL for simulation
print(CSTART1 + "MICROGRID P2P SIMULATION REPL" + CEND)
print(CSTART1 + "Command List" + CEND)
print("live --  run simulation indefinitely, printing prosumer stats at each timestep")
print("avg -- run multiple simulations, finding avg values across all simulations")
print("# -- step forward # amount of hours in the simulation")
print("pp -- print statistics for each prosumer")
print("pc -- print statistics for the coordinator")
print("pr -- print statistics for the retailer")
print("day -- print current day of simulation")
print("q -- quit the REPL")
print()
# getting starting variables
# num_prosumers must be less than number of names available
while True:
    num_prosumers = input("Enter number of prosumers for the simulation: ")
    try:
        num_prosumers = int(num_prosumers)
        break
    except ValueError:
        print("Invalid input.")
# suggested starting internal price: 4
while True:
    internal_price = input("Enter starting internal price for the simulation: ")
    try:
        internal_price = float(internal_price)
        break
    except ValueError:
        print("Invalid input.")
# suggested starting external price: 6
while True:
    external_price = input("Enter starting external price for the simulation: ")
    try:
        external_price = float(external_price)
        break
    except ValueError:
        print("Invalid input.")

# creating grid instance
grid = MicroGrid(num_prosumers, internal_price, external_price)

# starting main REPL for interaction
while True:
    print()
    inp = input("Enter a command: ")
    # exiting the simulation
    if inp == "q":
        break
    # calculating average stats over days number of days
    elif inp == "avg":
        while True:
            sims = input("Enter number of simulations: ")
            days = input("Enter number of days for each simulation: ")
            # catching invalid values
            try:
                sims = int(sims)
                days = int(days)
                # initializing "count" variables for summation
                pro_money_spent = [0.0] * num_prosumers
                pro_money_earned = [0.0] * num_prosumers
                co_money_exchanged = 0.0
                # running sims number of simulations, adding to counters
                for i in range(sims):
                    grid = MicroGrid(num_prosumers, internal_price, external_price)
                    grid.run_iterations(days)
                    for j, prosumer in enumerate(grid._prosumers):
                        pro_money_spent[j] += prosumer._money_spent
                        pro_money_earned[j] += prosumer._e_money_earned
                    co_money_exchanged += grid._coordinator._e_exchange
                # finding averages for each of the given stats
                averages1 = np.divide(np.asarray(pro_money_spent), sims)
                averages2 = np.divide(np.asarray(pro_money_earned), sims)
                averages3 = co_money_exchanged / sims
                # printing results to console
                for k, prosumer in enumerate(grid._prosumers):
                    print(CSTART3 + str(prosumer._name) + CEND)
                    print("average money spent on energy: " + str(averages1[k]))
                    print("average money earned through energy: " + str(averages2[k]))
                print(CSTART3 + str(grid._coordinator._name) + CEND)
                print("average energy exchanged with retailer: " + str(averages3))
            except ValueError:
                print("Invalid values.")
            break
        grid = MicroGrid(num_prosumers, internal_price, external_price)
    # running "live" simulation
    elif inp == "live":
        while True:
            grid.run_iterations(1)
            grid.print_prosumer_stats()
            time.sleep(1)
            print()
    # printing prosumer statistics
    elif inp == "pp":
        grid.print_prosumer_stats()
    # printing coordinator statistics
    elif inp == "pc":
        grid.print_coordinator_stats()
    # printing retailer statistics
    elif inp == "pr":
        grid.print_retailer_stats()
    # printing the surrent day of the simulation
    elif inp == "day":
        print("The current day of the simulation is: " + str(grid._time))
    # stepping ahead inp amount of days in simulation
    else:
        try:
            iterations = int(inp)
            grid.run_iterations(iterations)
        except ValueError:
            print("Invalid input.")

print(CSTART2 + "exiting..." + CEND)