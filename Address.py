class Address:
    def __init__(self, location, address):
        self.location = location
        self.address = address

    def get_location(self):
        return self.location

    def get_address(self):
        return self.address

    def set_location(self, new_location):
        self.location = new_location

    def set_address(self, new_address):
        self.address = new_address
