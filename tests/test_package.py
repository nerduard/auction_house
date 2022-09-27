import os
import sys

# append to sys path to be able to import line parser module
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import line_parser as lp

def run(path):
    file = open(path, 'r')
    # parse all the lines in the input file
    with open(path, "r") as file:
        for line in file:
            lp.parse_line(line)
    # clear listing collection dictionary for next input
    lp.lc.dict.clear()

# FUNCTIONAL TESTING
# Test the provided sample input
def test_sample(capsys):
    run("inputs/input.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n"
        "20|tv_1||UNSOLD|0.00|2|200.00|150.00\n"
    )


# Test that when second highest bid is lower
# than the reserve price, then price paid
# becomes the reserve price
def test_second_bid_lower_than_reserve_price(capsys):
    run("inputs/input2.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "20|raspberry_pi|8|SOLD|10.00|4|12.50|5.50\n"
    )

# Test that when higher than reserve price bid
# arrives before auction start date, it is not
# registered
def test_bid_before_auction_start(capsys):
    run("inputs/input3.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "12|macintosh||UNSOLD|0.00|0|0.00|0.00\n"
    )

# Test that when higher than reserve price bid
# arrives on auction start date, it is not
# registered
def test_bid_on_auction_start(capsys):
    run("inputs/input4.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "12|macintosh||UNSOLD|0.00|0|0.00|0.00\n"
    )
    
# Test that when 3 bids are placed and
# one of them is lower than the previous
# one, only 2 bids get registered
def test_2_valid_1_invalid_bids(capsys):
    run("inputs/input5.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "20|macintosh||UNSOLD|0.00|2|9.50|7.50\n"
    )
    
# Test that when there are at least 2 bids
# placed over the reserve price, then the 
# second highest bid becomes the price paid
def test_price_paid_at_least_2_bids_over_reserve(capsys):
    run("inputs/input6.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "20|macintosh|7|SOLD|14.50|5|21.00|5.50\n"
    )
    
# Test that when there is only one bid
# placed over the reserve price, then
# the price paid is the reserve price
def test_price_paid_1_bid_over_reserve(capsys):
    run("inputs/input7.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "20|macintosh|7|SOLD|10.00|5|21.00|5.50\n"
    )

# Test that when 2 bids are received at different times
# for the same amount, then the earliest
# bid wins the auction and the second one
# doesn't get registered
def test_2_equal_bids_at_different_times(capsys):
    run("inputs/input8.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "20|macintosh|5|SOLD|10.00|1|12.50|12.50\n"
    )
    
# Test that when 2 bids are received at the same time
# for the same amount, then the earliest
# bid wins the auction and the second one
# doesn't get registered
def test_2_equal_bids_at_the_same_time(capsys):
    run("inputs/input9.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "20|macintosh|5|SOLD|10.00|1|12.50|12.50\n"
    )
    
# Test the following scenario:
# - one iphone listing with 2 valid
# bids (one over reserve and one under),
# reserve price should be paid.
# - one macbook listing with 2 valid and
# one invalid bids, with all valid bids
# higher than reserve, therefore second
# highest bid amount should be paid.
def test_2_listings_scenario(capsys):
    run("inputs/input10.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "20|iphone|13|SOLD|100.00|2|110.00|60.00\n"
        "20|macbook|8|SOLD|75.50|2|175.50|75.50\n"
    )
    
# Test the following scenario:
# - one iphone listing with 2 valid
# bids (both under reserve price),
# therefore listing goes UNSOLD.
# - one macbook listing with 1 valid and
# 2 subsequent invalid bids, with the valid
# bid under the reserve price, therefore
# listing goes UNSOLD.
def test_2_listings_scenario_unsold(capsys):
    run("inputs/input11.txt")
    captured = capsys.readouterr()
    assert captured.out == (
        "20|iphone||UNSOLD|0.00|2|99.00|60.00\n"
        "20|macbook||UNSOLD|0.00|1|74.00|74.00\n"
    )


