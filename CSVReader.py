import csv

from Address import Address
from Package import Package


class CSVReader:

    # helper method to read and load addresses
    @staticmethod
    def load_addresses(file_name):
        # initialize an empty array
        address_list = []
        with open(file_name) as addresses:
            # separate columns by ","
            address_data = csv.reader(addresses, delimiter=',')
            # skip first row.
            next(address_data)
            for row in address_data:
                # initialize a variable which has [location, address] format
                address = Address(row[0], row[1])
                # add it to the address_list
                address_list.append(address)
        return address_list


    @staticmethod
    def load_packages(file_name, hash_table):
        # initialize an empty list
        package_list = []
        # open the CSV file and refer to it as packages
        with open(file_name) as packages:
            # read the csv file and separate columns by ","
            package_data = csv.reader(packages, delimiter=',')
            # skip the first row which contains headers.
            next(package_data)
            for row in package_data:
                # extract the package attributes
                package_id = row[0]
                package_destination = row[1]
                package_city = row[2]
                package_city = row[4]
                package_deadline = row[5]
                package_weight = int(row[6])
                package_note = row[7]
                package_truck_affinity = row[8]
                # default delivery_status
                package_delivery_status = "at the hub"

                # update delivery status if package_note contains "Delayed" as a substring
                if "Delayed" in package_note:
                    package_delivery_status = "delayed"

                # instantiate a package with the extracted data
                package = Package(package_id, package_destination, package_deadline, package_city, package_city,package_weight,package_delivery_status, package_note, package_truck_affinity)
                # add the package to the initialized list
                package_list.append(package)

        # add each package to the hash table passed in as an argument
        for package in package_list:
            hash_table.set_package(package.get_id(), package)


    @staticmethod
    def load_distances(file_name):
        # initialize an empty list
        data = []
        # open the csv file
        with open(file_name) as distances:
            # read the csv and separate columns by ","
            distance_data = csv.reader(distances, delimiter=',')
            # transform the data to a list which will now be a 2D list
            data = list(distance_data)
        return data



