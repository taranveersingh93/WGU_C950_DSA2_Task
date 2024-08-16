class Truck:
    def __init__(self, truck_id, total_capacity=16):
        # initialized with the given values
        self.id = truck_id
        self.total_capacity = total_capacity
        self.reserved_capacity = 0
        self.undelivered_packages = []
        self.delivered_packages = []
        self.miles = 0
        self.current_address = "HUB"\
        # will be set when truck departs
        self.departure_time = None
        # will be set at every delivery
        self.last_recorded_time = None
        # will be used for status checks for particular timed queries.
        self.mileage_timestamps = []

    # getter for id
    def get_id(self):
        return self.id

    # append package id to undelivered_packages
    def load_package(self, package_id):
        self.undelivered_packages.append(package_id)

    # move package id from undelivered packages to delivered packages array
    def deliver_package(self, package_id):
        if package_id in self.undelivered_packages:
            self.undelivered_packages.remove(package_id)
            self.delivered_packages.append(package_id)

    # getter for current address
    def get_current_address(self):
        return self.current_address

    # getter for total capacity
    def get_total_capacity(self):
        return self.total_capacity

    # setter for total capacity
    def set_total_capacity(self, total_capacity):
        self.total_capacity = total_capacity

    # get the number of available capacity on truck
    def get_available_capacity(self):
        return self.total_capacity - self.reserved_capacity

    # setter for reserved capacity. Used when processing "delayed" package data
    def set_reserved_capacity(self, new_reserved_capacity):
        self.reserved_capacity = new_reserved_capacity

    # getter for reserved capacity
    def get_reserved_capacity(self):
        return self.reserved_capacity

    # get package IDs of undelivered packages
    def get_package_ids(self):
        return self.undelivered_packages

    # get package IDs of delivered packages
    def get_delivered_package_ids(self):
        return self.delivered_packages

    # setter for departure time
    def set_departure_time(self, departure_time):
        self.departure_time = departure_time

    # getter fpr departure time
    def get_departure_time(self):
        return self.departure_time

    # getter for last recorded time
    def get_last_recorded_time(self):
        if self.last_recorded_time is not None:
            return self.last_recorded_time
        else:
            return self.departure_time

    # setter for current address. updates on every delivery
    def set_current_address(self, address):
        self.current_address = address

    # add [timestamp, mileage] to mileage_timestamps array.
    # add the miles argument to the existing miles attribute

    def add_mileage_timestamp(self, timestamp, miles):
        self.mileage_timestamps.append([timestamp, miles])
        self.miles += miles
        self.last_recorded_time = timestamp

    # loop through the mileage_timestamps to get total miles after the deliveries are done
    def get_final_mileage(self):
        total_miles = 0
        for timestamp, miles in self.mileage_timestamps:
            total_miles += miles
        return total_miles

    # use a query time to compare with the timestamps and get the mileage at that particular point in time
    def get_mileage_at(self, query_time):
        total_miles = 0
        for timestamp, miles in self.mileage_timestamps:
            if timestamp >= query_time:
                return total_miles
            else:
                total_miles += miles
        return total_miles
