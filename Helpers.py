import datetime


class Helpers:
    @staticmethod
    def load_package_on_truck(package_value, truck, package_table):
        # load the package on the truck if the package is "at the hub".
        # essentially all packages that aren't "delayed" can be loaded.
        if package_value.delivery_status == "at the hub":
            package_id = package_value.get_id()
            truck_id = truck.get_id()
            # add the package id to the truck's undelivered_packages array.
            truck.load_package(package_id)
            # reduce the truck's total capacity
            truck.set_total_capacity(truck.get_total_capacity() - 1)
            # retrieve the package from the hash table
            package = package_table.get_package(package_id)
            # update the truck id in the package object. This does not update the package entry in the hashtable
            package.set_truck_id(truck_id)
            # update the delivery status of package to "loaded"
            package.set_delivery_status("loaded")
            # update the package entry in the hash table
            package_table.set_package(package_id, package)

    @staticmethod
    def load_delayed_package_on_truck(package_value, truck, package_table):
        package_id = package_value.get_id()
        # load the package on the truck's "undelivered packages" array.
        truck.load_package(package_id)
        truck_id = truck.get_id()
        # decrement the truck's "reserved capacity". Different from "total capacity".
        # This helps because a package is added to a truck if its available_capacity is > 0.
        # The available capacity = total_capacity - reserved_capacity.
        # When a "delayed" package entry is processed, the truck's  "reserved_capacity" is incremented.
        # So when the delayed package is loaded, it makes sense to decrement the reserved_capacity.
        truck.set_reserved_capacity(truck.get_reserved_capacity() - 1)
        # retrieve the package
        package = package_table.get_package(package_value.get_id())
        package.set_truck_id(truck_id)
        # set the delivery status to "loaded"
        package.set_delivery_status("loaded")
        # update the package in the hashtable
        package_table.set_package(package.get_id(), package)

    @staticmethod
    def load_trucks_by_affinity(package_table, truck1, truck2, truck3):
        # get a list of all packages stored in the package table
        all_packages = package_table.get_all_packages()
        for package in all_packages:
            # if the package is delayed and its supposed to go to truck 2, add truck 2's reserved_capacity but don't load the package
            if package.get_delivery_status() == "delayed" and package.get_truck_affinity() == str(truck2.get_id()):
                truck2.set_reserved_capacity(truck2.get_reserved_capacity() + 1)
            # if the truck has available_capacity (total_capacity - reserved_capacity) and its status is "at the hub", load the package on the relevant truck
            elif truck1.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub" and package.get_truck_affinity() == str(truck1.get_id()):
                Helpers.load_package_on_truck(package, truck1, package_table)
            elif truck2.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub" and package.get_truck_affinity() == str(truck2.get_id()):
                Helpers.load_package_on_truck(package, truck2, package_table)
            elif truck3.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub" and package.get_truck_affinity() == str(truck3.get_id()):
                Helpers.load_package_on_truck(package, truck3, package_table)

    @staticmethod
    def load_trucks_by_EOD(package_table, truck1, truck2, truck3):
        # get all packages in the package table
        all_packages = package_table.get_all_packages()
        for package in all_packages:
            # if the deadline is "EOD" and other conditions apply, add the package to the truck
            if package.deadline == "EOD":
                # load the EOD packages to truck 3 first as it leaves last.
                if truck3.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub":
                    Helpers.load_package_on_truck(package, truck3, package_table)
                elif truck2.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub":
                    Helpers.load_package_on_truck(package, truck2, package_table)
                elif truck1.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub":
                    Helpers.load_package_on_truck(package, truck1, package_table)

    @staticmethod
    def filter_packages_by_status(packages, status):
        # filter packages by the delivery status. This method is used while the packages are being delivered programatically.
        # the status' used in this method are different from that in "filter_packages_by_status_with_time".
        # this method is used when the program is executing, not when the user is getting packages by status.
        packages_with_status = [package for package in packages if package.get_delivery_status() == status]
        return packages_with_status

    @staticmethod
    def filter_packages_by_status_with_time(packages, status, current_time, trucks):
        packages_with_status = []
        # this method is similar to but different from "filter_packages_by_status"
        for package in packages:
            truck_id = package.get_truck_id()
            truck = trucks[int(truck_id)-1]
            truck_departure_time = truck.get_departure_time()
            # use the package method that compares the time of the query against the truck's departure time.
            # if "package.check_status_against_time" method returns a value matching the status argument, the package is added to the packages_with_status
            if package.check_status_against_time(current_time, truck_departure_time) == status.lower():
                packages_with_status.append(package)
        return packages_with_status

    @staticmethod
    def load_delayed_packages(package_table, truck):
        # get all the packages in the hashtable
        all_packages = package_table.get_all_packages()
        # get all the packages marked "delayed". Again, this uses the "packages_by_status" method which is used by the program within the first few seconds of execution.
        # (contd.) that's when the truck is loading and delivering the packages.
        delayed_packages = Helpers.filter_packages_by_status(all_packages, "delayed")
        for package in delayed_packages:
            # load each delayed package on the truck.
            Helpers.load_delayed_package_on_truck(package, truck, package_table)

    @staticmethod
    def get_package_distance(destination_address, current_address, address_list, distance_matrix):
        # initialize both indices as 0. These will be used to get a value from the distance matrix which is a 2D array
        current_address_index = 0
        destination_index = 0
        # loop through the address list which is an array of array-items [location, address]
        for i, address in enumerate(address_list):
            # if the current_address argument is a substring of the row being scanned, set current_address_index = i
            if current_address in address.get_address():
                current_address_index = i
            # if the destination_address is a substring of the row being scanned, set destination_address_index = i
            if destination_address in address.get_address():
                destination_index = i
        # locate the distance from the distance matrix.
        distance = distance_matrix[current_address_index][destination_index]
        # if the distance from the distance_matrix is an empty string, use the mirror image by inverting the indices.
        if distance == "":
            distance = distance_matrix[destination_index][current_address_index]
        # removing an erroneous string in an edge case.
        distance = distance.replace('ï»¿', '')
        return float(distance)

    @staticmethod
    def get_packages_with_distance(packages, current_address, address_list, distance_matrix):
        # for each package in "packages" return an array of the form [package, distance from current_address]
        packages_with_distance = [(package, Helpers.get_package_distance(package.get_address(), current_address, address_list, distance_matrix)) for package in packages]
        return packages_with_distance

    @staticmethod
    def sort_packages_by_distance(packages_with_distance):
        # the second item in the element is the distance so sort the array using that.
        sorted_packages = sorted(packages_with_distance, key=lambda package:package[1])
        # extract only the package objects after the array has been sorted by distance.
        package_objects = [package[0] for package in sorted_packages]
        return package_objects

    @staticmethod
    def load_trucks_by_distance(package_table, truck1, truck2, truck3, address_list, distance_matrix):
        # get all packages from the package table
        all_packages = package_table.get_all_packages()
        # filter them all based on "at the hub" status
        packages_to_load = Helpers.filter_packages_by_status(all_packages, "at the hub")
        # use the filtered list to then return a list which has distances as well. [[package, distance], [package2, distance2],...]
        packages_with_distance = Helpers.get_packages_with_distance(packages_to_load, "HUB", address_list, distance_matrix)
        # sort the packages by distance and get an array of packages only.
        sorted_package_values = Helpers.sort_packages_by_distance(packages_with_distance)

        # load the packages in the order of truck 1, 2, 3.
        for package_value in sorted_package_values:
            if truck1.get_available_capacity() > 0:
                Helpers.load_package_on_truck(package_value, truck1, package_table)
            elif truck2.get_available_capacity() > 0:
                Helpers.load_package_on_truck(package_value, truck2, package_table)
            elif truck3.get_available_capacity() > 0:
                Helpers.load_package_on_truck(package_value, truck3, package_table)

    @staticmethod
    def load_trucks(package_table, truck1, truck2, truck3, address_list, distance_matrix):
        # the orchestrator method that calls the helper methods.
        # it first loads packages by truck affinity (takes care of special notes)
        Helpers.load_trucks_by_affinity(package_table, truck1, truck2, truck3)
        # load packages by EOD in truck 3, then truck 2, then truck 1
        Helpers.load_trucks_by_EOD(package_table, truck1, truck2, truck3)
        # load packages by distance. Closest to the hub are loaded in truck1, then truck 2 then truck 3
        Helpers.load_trucks_by_distance(package_table, truck1, truck2, truck3, address_list, distance_matrix)

    @staticmethod
    def get_nearest_package_id(current_address, undelivered_package_ids, package_table, address_list, distance_matrix):
        # placeholder high number value
        min_distance = 999999
        min_package_id = None
        for package_id in undelivered_package_ids:
            # get package from hash table
            package = package_table.get_package(package_id)
            # use helper method to get the distance from current address to the package in the iteration
            distance = Helpers.get_package_distance(package.get_address(), current_address, address_list, distance_matrix)
            # if the calculated new distance is less than the running min_distance, update the min_distance.
            # also update the min_package_id
            if min_distance > distance:
                min_distance = distance
                min_package_id = package_id
        return [min_package_id, min_distance]

    @staticmethod
    def deliver_packages(package_table, truck, address_list, distance_matrix):
        # while the truck has undelivered packages
        while len(truck.get_package_ids()) > 0:
            # get truck's current location
            current_address = truck.get_current_address()
            undelivered_package_ids = truck.get_package_ids()
            # destructure and get the nearest_package_id and the distance
            [nearest_package_id, distance] = Helpers.get_nearest_package_id(current_address, undelivered_package_ids, package_table, address_list, distance_matrix)
            # get the package from the hashtable
            package = package_table.get_package(nearest_package_id)
            # add [timestamp, miles] to a list "mileage_timestamps" in truck. This list comes handy if user wants to get truck mileage at a particular timestamp
            # this method internally also updates the truck's last_recorded_time which will be used later in this method
            truck.add_mileage_timestamp(truck.get_last_recorded_time() + datetime.timedelta(hours=distance/18), distance)
            # update the truck's current address to the active package's delivery address
            truck.set_current_address(package.get_address())
            # move the package id from undelivered_packages to delivered_packages in truck.
            truck.deliver_package(nearest_package_id)
            # update the package status
            package.set_delivery_status("delivered")
            # mark the package's delivery time
            package.set_delivery_time(truck.get_last_recorded_time())
        # once the packages are delivered and the truck has no more undelivered packages, return to the hub.
        # calculate the distance from the truck's last "current_location" to "HUB"
        distance_to_hub = Helpers.get_package_distance("HUB", truck.get_current_address(), address_list, distance_matrix)
        # add the mileage timestamp to the truck.
        truck.add_mileage_timestamp(truck.get_last_recorded_time() + datetime.timedelta(hours=distance_to_hub/18), distance_to_hub)
        # update the current address to "HUB"
        truck.set_current_address("HUB")