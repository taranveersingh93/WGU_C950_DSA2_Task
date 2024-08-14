class Package:
    def __init__(self, id, address, deadline, city, zip_code, weight, delivery_status, note, truck_affinity):
        self.id = id
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

    def get_delivery_status(self):
        return self.delivery_status

    def set_delivery_status(self, status):
        self.delivery_status = status

    def get_truck_affinity(self):
        return self.truck_affinity
