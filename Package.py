class Package:
    def __init__(self, id, address, deadline, city, zipCode, weight, deliveryStatus, note, truckAffinity):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipCode = zipCode
        self.weight = weight
        self.deliveryStatus = deliveryStatus
        self.note = note
        self.truckAffinity = truckAffinity

    def getId(self):
        return self.id

    def get_address(self):
        return self.address

    def get_deliveryStatus(self):
        return self.deliveryStatus

    def set_deliveryStatus(self, status):
        self.deliveryStatus = status

    def get_truckAffinity(self):
        return self.truckAffinity