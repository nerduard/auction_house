from objects.ListingCollection import ListingCollection
from objects.Listing import Listing
from objects.Bid import Bid

# to store all listings
lc = ListingCollection()
# to keep track of current time
current_time = 0

# parse each line
def parse_line(line):
    input_elements = line.split('|')

    # if input is new listing
    if len(input_elements) == 6 and input_elements[2] == "SELL":
        try:
            current_time = int(input_elements[0])
            timestamp = current_time
            user_id = int(input_elements[1])
            item = str(input_elements[3])
            reserve_price = float(input_elements[4])
            close_time = int(input_elements[5])
        except:
            print("Error occurred whilst converting input elements to relevant object attribute types.")

        listing = Listing(timestamp, user_id, item,
                          reserve_price, close_time)
        lc.add(listing)

    # if input is new bid
    if len(input_elements) == 5 and input_elements[2] == "BID":
        try:
            current_time = int(input_elements[0])
            timestamp = current_time
            user_id = int(input_elements[1])
            item = str(input_elements[3])
            bid_amount = float(input_elements[4])
        except:
            print("Error occurred whilst converting input elements to relevant object attribute types.")

        bid = Bid(timestamp, user_id, item, bid_amount)
        
        # we perform bid checks to see if it is valid
        # and whether it gets added to the relevant listing
        isBidValid = True

        # cannot bid on an item that hasn't been auctioned yet
        if item not in lc.dict:
            isBidValid = False
        else:
            # bid cannot arrive before or on the auction start time
            # or after the close time
            if bid.timestamp <= lc.dict[item].timestamp or bid.timestamp > lc.dict[item].close_time:
                isBidValid = False

            # bid should be larger than any previous bids.
            # if listing has at least one previous bid and
            # it is larger or equal to our current bid, then
            # the current bid won't be added
            bids_no = len(lc.dict[item].bids)
            if bids_no > 0 and lc.dict[item].bids[bids_no - 1].bid_amount >= bid.bid_amount:
                isBidValid = False

        # add bid to listing if none of the conditions above apply
        if isBidValid:
            lc.dict[item].bids.append(bid)

    # if input is a heartbeat
    if len(input_elements) == 1:
        current_time = int(input_elements[0])
        update_state(current_time)

# update object attributes (and stats) for all relevant listings
def update_state(current_time):
    for key in lc.dict.keys():
        listing = lc.dict[key]
        if listing.ongoing is True and listing.close_time <= current_time:
            listing.ongoing = False
            update_listing_fields(listing)
            print_ended_listing(listing)


def update_listing_fields(listing):
    # when there are at least 2 bids already placed
    if len(listing.bids) >= 2:
        # and most recent bid is higher than the reserve price
        if listing.bids[len(listing.bids)-1].bid_amount >= listing.reserve_price:
            listing.winner = listing.bids[len(listing.bids)-1].user
            # price paid is second highest bid if second highest bid is 
            # higher or equal to the reserve price
            if listing.bids[len(listing.bids)-2].bid_amount >= listing.reserve_price:
                listing.price_paid = listing.bids[len(listing.bids)-2].bid_amount
            # otherwise price_paid becomes the reserve price
            else:
                listing.price_paid = listing.reserve_price
            listing.state = "SOLD"
            listing.highest_bid = listing.bids[len(listing.bids)-1].bid_amount
            listing.lowest_bid = listing.bids[0].bid_amount
        # else if no bids go beyond the reserve price
        else:
            listing.state = "UNSOLD"
            listing.highest_bid = listing.bids[len(listing.bids)-1].bid_amount
            listing.lowest_bid = listing.bids[0].bid_amount
    # when there is exactly one bid placed
    elif len(listing.bids) == 1:
        # and it's higher than the reserve price
        if listing.bids[0].bid_amount >= listing.reserve_price:
            listing.winner = listing.bids[0].user
            listing.price_paid = listing.reserve_price
            listing.state = "SOLD"
            listing.highest_bid = listing.bids[0].bid_amount
            listing.lowest_bid = listing.highest_bid
        # else if it's not higher than reserve price
        else:
            listing.state = "UNSOLD"
            listing.highest_bid = listing.bids[0].bid_amount
            listing.lowest_bid = listing.highest_bid
    # if there are no bids placed
    else:
        listing.state = "UNSOLD"


def print_ended_listing(listing):
    global lines_printed
    # when listing is 'SOLD', we need to access winner id
    if listing.state == "SOLD":
        to_print = str(listing.close_time) + '|' + listing.item + \
            '|' + str(listing.winner.id) + '|' + listing.state + '|' + str(format(listing.price_paid, ".2f")) + \
            '|' + str(len(listing.bids)) + '|' + str(format(listing.highest_bid, ".2f")) + \
            '|' + str(format(listing.lowest_bid, ".2f"))
    # when listing is not 'SOLD', winner id becomes ''
    else:
        to_print = str(listing.close_time) + '|' + listing.item + \
            '|' + '' + '|' + listing.state + '|' + str(format(listing.price_paid, ".2f")) + \
            '|' + str(len(listing.bids)) + '|' + str(format(listing.highest_bid, ".2f")) + \
            '|' + str(format(listing.lowest_bid, ".2f"))

    print(to_print)
