# models a coordinator, keeping track of internal and external prices
class Coordinator:

    def __init__(self, name, p_external, e_bid, p_internal, e_exchange):
        self._name = name
        # environment vars
        self._p_external = p_external 
        self._e_bid = e_bid 
        # action vars
        self._p_internal = p_internal 
        self._e_exchange = e_exchange
    
    # updating the internal price set by the coordinator -- placeholder
    def update_internal_price(self):
        self._p_internal = self._p_internal