class Truck:
    def __init__(self, truck_id, total_capacity=16):
        self.id = truck_id
        self.total_capacity = total_capacity
        self.reserved_capacity = 0
        self.packages = []
        self.miles = 0
        self.current_location = "HUB"

    def get_id(self):
        return self.id

    def add_package(self, package):
        self.packages.append(package)

    def get_miles(self):
        return self.miles

    def get_total_capacity(self):
        return self.total_capacity

    def set_total_capacity(self, total_capacity):
        self.total_capacity = total_capacity

    def get_available_capacity(self):
        return self.total_capacity - self.reserved_capacity

    def set_reserved_capacity(self, new_reserved_capacity):
        self.reserved_capacity = new_reserved_capacity

    def get_reserved_capacity(self):
        return self.reserved_capacity

    def get_packages(self):
        return self.packages

