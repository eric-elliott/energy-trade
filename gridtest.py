import numpy as np
import pandapower as pp
import pandapower.networks as pn
# import pandapower.shortcircuit as sc
# import pandapower.plotting as plot
# from soltrade.models import User

net = pn.create_cigre_network_mv(with_der=False)
# net=  pn.create_kerber_vorstadtnetz_kabel_1()
print(net.bus)

# use this for indices
# print(list(range(3, 295, 2)))

# user = User.query.filter_by(username="alice").first()
# print(user.id)

