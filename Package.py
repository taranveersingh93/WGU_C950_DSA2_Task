import datetime


class Package:
    def __init__(self, id, address, deadline, city, zip_code, weight, delivery_status, note, truck_affinity):
        self.id = id
        self.truck_id = None
        self.delivery_time = None
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.delivery_status = delivery_status
        self.note = note
        self.truck_affinity = truck_affinity

    def get_id(self):
        return self.id

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_delivery_status(self):
        return self.delivery_status

    def set_delivery_status(self, status):
        self.delivery_status = status

    def set_delivery_time(self, time):
        self.delivery_time = time

    def get_truck_affinity(self):
        return self.truck_affinity

    def get_truck_id(self):
        return self.truck_id

    def set_truck_id(self, truck_id):
        self.truck_id = truck_id

    def check_status_against_time(self, query_time, departure_time):
        if self.id == "6" or self.id == "25" or self.id == "28" or self.id == "32":
            if query_time < datetime.timedelta(hours=9, minutes=5):
                return "delayed"
        if query_time < self.delivery_time:
            if query_time < departure_time:
                return "loaded"
            if query_time > departure_time:
                return "on its way"
        else:
            return "delivered"

    def get_status(self, query_time, departure_time):
        status = self.check_status_against_time(query_time, departure_time)
        if status == "delayed":
            return f"The package {self.id} is delayed.\n Truck #: {self.truck_id} \n Destination: {self.address} \n Deadline: {self.deadline}"
        elif self.id == "9" and query_time < datetime.timedelta(hours=10, minutes=20):
            return f"The package {self.id} is loaded.\n Truck #: {self.truck_id} \n Destination: 300 State St \n Deadline: {self.deadline}"
        elif status == "loaded":
            return f"The package {self.id} is loaded. \n Truck #: {self.truck_id} \n Departure Time: {departure_time} \n Destination: {self.address} \n Deadline: {self.deadline}"
        elif status == "on its way":
            return f"The package {self.id} is on its way. \n Truck #: {self.truck_id} \n Departure Time: {departure_time} \n Destination: {self.address} \n Deadline: {self.deadline}"
        else:
            return f"The package {self.id} was delivered. \n Truck #: {self.truck_id} \n Departure Time: {departure_time} \n Destination: {self.address} \n Deadline: {self.deadline} \n Delivered at: {self.delivery_time}"
