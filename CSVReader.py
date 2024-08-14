import csv

from Address import Address
from Package import Package


class CSVReader:
    @staticmethod
    def load_addresses(file_name):
        address_list = []
        with open(file_name) as addresses:
            address_data = csv.reader(addresses, delimiter=',')
            next(address_data)
            for row in address_data:
                address = Address(row[0], row[1])
                address_list.append(address)
        return address_list

    @staticmethod
    def load_packages(file_name, hash_table):
        package_list = []
        with open(file_name) as packages:
            package_data = csv.reader(packages, delimiter=',')
            next(package_data)
            for row in package_data:
                package_id = row[0]
                package_destination = row[1]
                package_city = row[2]
                package_city = row[4]
                package_deadline = row[5]
                package_weight = int(row[6])
                package_note = row[7]
                package_truck_affinity = row[8]
                package_delivery_status = "at the hub"

                if "Delayed" in package_note:
                    package_delivery_status = "delayed"

                package = Package(package_id, package_destination, package_deadline, package_city, package_city,package_weight,package_delivery_status, package_note, package_truck_affinity)
                package_list.append(package)
                # if packageTruckAffinity == "1" or packageTruckAffinity == "2" or packageTruckAffinity == "3":
                #     package_listWithAffinity.append(package)
                # else:
                #     package_listWithoutAffinity.append(package)
        for package in package_list:
            hash_table.set_package(package.get_id(), package)
        # for package in package_listWithAffinity:
        #     hash_table.addPackage(package)
        # for package in package_listWithoutAffinity:
        #     hash_table.addPackage(package)

    @staticmethod
    def load_distances(file_name):
        data = []
        with open(file_name) as distances:
            distance_data = csv.reader(distances, delimiter=',')
            data = list(distance_data)
        return data



