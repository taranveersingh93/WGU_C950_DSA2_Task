class Truck:
    def __init__(self, truck_id, total_capacity=16):
        self.id = truck_id
        self.total_capacity = total_capacity
        self.reserved_capacity = 0
        self.undelivered_packages = []
        self.delivered_packages = []
        self.miles = 0
        self.current_address = "HUB"
        self.departure_time = None
        self.last_recorded_time = None

    def get_id(self):
        return self.id

    def load_package(self, package_id):
        self.undelivered_packages.append(package_id)

    def deliver_package(self, package_id):
        if package_id in self.undelivered_packages:
            self.undelivered_packages.remove(package_id)
            self.delivered_packages.append(package_id)

    def get_current_address(self):
        return self.current_address

    def get_miles(self):
        return self.miles

    def set_miles(self, miles):
        self.miles = miles

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

    def get_package_ids(self):
        return self.undelivered_packages

    def set_departure_time(self, departure_time):
        self.departure_time = departure_time

    def get_last_recorded_time(self):
        if self.last_recorded_time is not None:
            return self.last_recorded_time
        else:
            return self.departure_time

    def set_last_recorded_time(self, last_recorded_time):
        self.last_recorded_time = last_recorded_time

    def set_current_address(self, address):
        self.current_address = address

