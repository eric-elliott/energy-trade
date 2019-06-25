# models a retailer, keeping track of external price, as well as
# buying price
class Retailer:

    def __init__(self, name, r_buy, p_external):
        self._name = name
        # setting price energy is sold at and bought at from coordinator
        self._buy_for = r_buy
        self._sell_for = p_external

    # updating external price set by retailer -- placeholder, not sure if this should
    # be a constant or variable value
    def update_external_price(self):
        self._sell_for = self._sell_for