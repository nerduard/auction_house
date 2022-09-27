# timestamp|user_id|action|item|bid_amount
# Object to represent an individual bid
from objects.User import User

class Bid:
    def __init__(self, timestamp, user_id, item, bid_amount):
        self.timestamp = timestamp # integer
        self.user = User(user_id) # integer
        self.item = item # string
        self.bid_amount = bid_amount # float