class Address:
    # Constructor
    def __init__(self, location, address):
        self.location = location
        self.address = address

    # getter for location
    def get_location(self):
        return self.location

    # getter for address
    def get_address(self):
        return self.address

    # setter for location
    def set_location(self, new_location):
        self.location = new_location

    # setter for address
    def set_address(self, new_address):
        self.address = new_address
