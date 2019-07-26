from soltrade.models import Offer, Request
from soltrade.powergrid import PowerGrid
from sqlalchemy import desc

"""
method for checking if offers can be hosted by grid
"""
def process_offers():
    powergrid = PowerGrid()
    powergrid.check_offers()


"""
method to clear offers after end of day
"""
def clear_offers_bids():
    Offer.query().delete()
    
    