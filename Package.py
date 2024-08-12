class Package:
    def __init__(self, id, address, deadline, city, zipCode, weight, deliveryStatus, truckAffinity):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipCode = zipCode
        self.weight = weight
        self.deliveryStatus = deliveryStatus
        self.truckAffinity = truckAffinity