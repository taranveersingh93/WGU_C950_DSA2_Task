import datetime


class Package:
    def __init__(self, id, address, deadline, city, zip_code, weight, delivery_status, note, truck_affinity):
        # initialize package with the said values
        self.id = id
        # initialized as none. Updated when a package is loaded on a truck
        self.truck_id = None
        # initialized as none. Updated when delivered
        self.delivery_time = None
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        # used for programmatic status checks
        self.delivery_status = delivery_status
        self.note = note
        # manually entered values in the csv to have packages loaded on certain trucks
        self.truck_affinity = truck_affinity

    # getter for id
    def get_id(self):
        return self.id

    # getter for package delivery address
    def get_address(self):
        return self.address

    # setter for address
    def set_address(self, address):
        self.address = address

    # getter for delivery status (programatic status checks, not the status displayed on UI)
    def get_delivery_status(self):
        return self.delivery_status

    # setter for delivery status
    def set_delivery_status(self, status):
        self.delivery_status = status

    # setter for delivery time set at delivery.
    def set_delivery_time(self, time):
        self.delivery_time = time

    # getter for truck affinity
    def get_truck_affinity(self):
        return self.truck_affinity

    # getter for truck id
    def get_truck_id(self):
        return self.truck_id

    # setter for truck id. Used while loading packages to trucks.
    def set_truck_id(self, truck_id):
        self.truck_id = truck_id

    # the method used for status displays on UI
    def check_status_against_time(self, query_time, departure_time):
        # edge case of the delayed packages
        if self.id == "6" or self.id == "25" or self.id == "28" or self.id == "32":
            if query_time < datetime.timedelta(hours=9, minutes=5):
                return "delayed"
        # if the time being queried for is less than the delivery time, the package can either be loaded or on its way
        if query_time < self.delivery_time:
            # if query time is before the truck's departure, the package is loaded
            if query_time < departure_time:
                return "loaded"
            # if query time is after the truck has departed, the package is on its way
            if query_time >= departure_time:
                return "on its way"
        # if nothing else matches, the package is delivered
        else:
            return "delivered"

    def get_status(self, query_time, departure_time):
        status = self.check_status_against_time(query_time, departure_time)
        # generate appropriate sentences corresponding to each status
        if status == "delayed":
            return f"Package {self.id}: delayed.\t Truck: {self.truck_id} \t Destination: {self.address} \t Deadline: {self.deadline}"
        elif self.id == "9" and query_time < datetime.timedelta(hours=10, minutes=20):
            return f"Package {self.id}: loaded.\t Truck: {self.truck_id} \t Destination: 300 State St \t Deadline: {self.deadline}"
        elif status == "loaded":
            return f"Package {self.id}: loaded. \t Truck: {self.truck_id} \t Departure Time: {departure_time} \t Destination: {self.address} \t Deadline: {self.deadline}"
        elif status == "on its way":
            return f"Package {self.id}: on its way. \t Truck: {self.truck_id} \t Departure Time: {departure_time} \t Destination: {self.address} \t Deadline: {self.deadline}"
        else:
            return f"Package {self.id}: delivered. \t Truck: {self.truck_id} \t Departure Time: {departure_time} \t Destination: {self.address} \t Deadline: {self.deadline} \t Delivery: {self.delivery_time}"
