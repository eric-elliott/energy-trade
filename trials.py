import numpy as np
from soltrade import db
from soltrade.models import User, Offer, Request, Group
from random import uniform
from random import shuffle
import pandapower as pp
import pandapower.networks as pn
import pandapower.plotting as plot

def violations(net):
    pp.runpp(net)
    line_percent = net.res_line.loading_percent.max()
    trafo_percent = net.res_trafo.loading_percent.max()
    bus_vm_pu = net.res_bus.vm_pu.max()
    measurements = [line_percent, trafo_percent, bus_vm_pu]
    if net.res_line.loading_percent.max() > 50:
        return [True, "Line \n Overloading", measurements]
    elif net.res_trafo.loading_percent.max() > 50:
        return [True, "Transformer \n Overloading", measurements]
    elif net.res_bus.vm_pu.max() > 1.04:
        return [True, "Voltage \n Violation", measurements]
    else:
        return [False, None, measurements]

# number of panels each user owns
panels = 30
# number of days trading
days = 31
# daily energy needed
energy_needed = 28.5
iter_violations = []
iter_line_percent = []
iter_trafo_percent = []
iter_bus_vm_pu = []
iter_enough = []
iterations = 5
for i in range(iterations):
    # querying users — IDs start from 1
    ex_net = pn.create_kerber_vorstadtnetz_kabel_1()
    user_buses = {}
    users = User.query.all()
    for user in users:
        user_buses[user.id] = np.random.choice(ex_net.load.bus.values)
    total_line_percent = 0
    total_trafo_percent = 0
    total_bus_vm_pu = 0
    total_violations = 0
    total_days_wo_enough = 0
    times = 0
    # running possible trades
    for i in range(days):
        enough = False
        energy_defecit_surplus = {}
        user_need = {}
        user_excess = {}
        net_energy_users = {}
        total_available_energy = 0
        total_user_need = 0
        for user in users:
            # calculating random variable for variation
            fluctuation = uniform(.8, 1.25)
            # getting probable energy generated
            energy_generated = panels * fluctuation
            # finding energy needed today
            energy_needed_today = energy_needed * uniform(.9, 1.1)
            # calculating net energy — negative if energy needed
            net_energy = energy_generated - energy_needed_today
            net_energy_users[user.id] = net_energy
            if net_energy < 0:
                user_need[user.id] = abs(net_energy)
                total_user_need += abs(net_energy)
            else:
                user_excess[user.id] = net_energy
                total_available_energy += net_energy
        user_send = {}
        grid_net_energy = total_available_energy - total_user_need
        if grid_net_energy < 0:
            user_send = user_excess
            enough = False
        else:
            enough = True
            for id1, excess in user_excess.items():
                temp = total_user_need
                total_user_need -= excess
                if total_user_need < 0:
                    user_send[id1] = temp 
                else:
                    user_send[id1] = excess
        # running through power system
        net = pn.create_kerber_vorstadtnetz_kabel_1()
        for id1, send in user_send.items():
                violated, violation_type, measurements = violations(net)
                times += 1
                total_line_percent += measurements[0]
                total_trafo_percent += measurements[1]
                total_bus_vm_pu += measurements[2]
                if violated:
                    total_violations += 1
                    break
                else:
                    pp.create_sgen(net, user_buses[id1], -send/1000, q_mvar=0)
        if enough == False:
            total_days_wo_enough += 1
    iter_violations.append(total_violations)
    iter_line_percent.append(total_line_percent/times)
    iter_trafo_percent.append(total_trafo_percent/times)
    iter_bus_vm_pu.append(total_bus_vm_pu/times)
    iter_enough.append(total_days_wo_enough)
    print(iter_line_percent)


avg_violations = sum(iter_violations)/iterations
avg_line_percent = sum(iter_line_percent)/iterations
avg_trafo_percent = sum(iter_trafo_percent)/iterations
avg_bus_vm_pu = sum(iter_bus_vm_pu)/iterations
avg_days_wo_enough = sum(iter_enough)/iterations
print("average number of violations:")
print(avg_violations)
print("average line percent:")
print(avg_line_percent)
print("average trafo percent:")
print(avg_trafo_percent)
print("average vm_pu:")
print(avg_bus_vm_pu)
print("average days where there wasn't enough energy:")
print(avg_days_wo_enough)
        

# energy_seconds = []
# energy_minutes = []
# energy_hours = []
# for rownum in range(1, sheet.nrows):
#     # getting energy produced past minute
#     if rownum % 60 == 0:
#         total_minute = sum(energy_seconds)
#         energy_minutes.append(total_minute)
#         energy_seconds = []
#     # getting energy produced past hour
#     if rownum % 3600 == 0:
#         total_hour = sum(energy_minutes)
#         energy_minutes = []
#         energy_hours.append(total_hour)
#     if rownum % 86400 == 0:
#         total_day = sum(energy_hours)
#         print(total_day)
#         energy_hours = []
#     currentkW = sheet.cell(rownum, 4).value
#     if type(currentkW) is float:
#         fluctuation = uniform(.8, 1.2)
#         currentkW = currentkW * fluctuation
#     else:
#         currentkW = 0
#     energy_seconds.append(currentkW)