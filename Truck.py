class Truck:
    def __init__(self, truckId, capacity=16):
        self.id = truckId
        self.capacity = capacity
        self.packages = []
        self.miles = 0

    def add_package(self, package):
        self.packages.append(package)

    def get_miles(self):
        return self.miles

    def get_capacity(self):
        return self.capacity

    def get_packages(self):
        return self.packages

