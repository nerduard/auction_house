# Object to represent a collection of listings using a dictionary

class ListingCollection:
    def __init__(self):
        self.dict = {}
        
    def add(self, listing):
        if listing.item not in self.dict:
            self.dict[listing.item] = listing
        
    def remove(self, listing):
        del self.dict[listing.item]