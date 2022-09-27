# timestamp|user_id|action|item|reserve_price|close_time
# Object to represent an individual listing
from objects.User import User

class Listing:
    def __init__(self, timestamp, user_id, item, reserve_price, close_time):
        self.timestamp = timestamp # integer
        self.user = User(user_id) # integer
        self.item = item # string
        self.reserve_price = reserve_price # float
        self.close_time = close_time # integer
        self.bids = []
        self.ongoing = True
        self.state = ""
        self.winner = None
        self.price_paid = 0.0
        self.highest_bid = 0.0
        self.lowest_bid = 0.0
