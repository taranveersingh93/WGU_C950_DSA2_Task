import datetime


class Helpers:
    @staticmethod
    def load_package_on_truck(package_value, truck, package_table):
        if package_value.delivery_status == "at the hub":
            package_id = package_value.get_id()
            truck_id = truck.get_id()
            truck.load_package(package_id)
            truck.set_total_capacity(truck.get_total_capacity() - 1)
            package = package_table.get_package(package_id)
            package.set_truck_id(truck_id)
            package.set_delivery_status("loaded")
            package_table.set_package(package_id, package)

    @staticmethod
    def load_delayed_package_on_truck(package_value, truck, package_table):
        package_id = package_value.get_id()
        truck.load_package(package_id)
        truck_id = truck.get_id()
        truck.set_reserved_capacity(truck.get_reserved_capacity() - 1)
        package = package_table.get_package(package_value.get_id())
        package.set_truck_id(truck_id)
        package.set_delivery_status("loaded")
        package_table.set_package(package.get_id(), package)

    @staticmethod
    def load_trucks_by_affinity(package_table, truck1, truck2, truck3):
        all_packages = package_table.iterate_packages()
        for package in all_packages:
            if package.get_delivery_status() == "delayed" and package.get_truck_affinity() == str(truck2.get_id()):
                truck2.set_reserved_capacity(truck2.get_reserved_capacity() + 1)
            elif truck1.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub" and package.get_truck_affinity() == str(truck1.get_id()):
                Helpers.load_package_on_truck(package, truck1, package_table)
            elif truck2.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub" and package.get_truck_affinity() == str(truck2.get_id()):
                Helpers.load_package_on_truck(package, truck2, package_table)
            elif truck3.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub" and package.get_truck_affinity() == str(truck3.get_id()):
                Helpers.load_package_on_truck(package, truck3, package_table)

    @staticmethod
    def load_trucks_by_EOD(package_table, truck1, truck2, truck3):
        all_packages = package_table.iterate_packages()
        for package in all_packages:
            if package.deadline == "EOD":
                if truck3.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub":
                    Helpers.load_package_on_truck(package, truck3, package_table)
                elif truck2.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub":
                    Helpers.load_package_on_truck(package, truck2, package_table)
                elif truck1.get_available_capacity() > 0 and package.get_delivery_status() == "at the hub":
                    Helpers.load_package_on_truck(package, truck1, package_table)

    @staticmethod
    def filter_packages_by_status(packages, status):
        packages_with_status = [package for package in packages if package.get_delivery_status() == status]
        return packages_with_status

    @staticmethod
    def filter_packages_by_status_with_time(packages, status, current_time, trucks):
        packages_with_status = []
        for package in packages:
            truck_id = package.get_truck_id()
            truck = trucks[int(truck_id)-1]
            truck_departure_time = truck.get_departure_time()
            if package.check_status_against_time(current_time, truck_departure_time) == status.lower():
                packages_with_status.append(package)
        return packages_with_status

    @staticmethod
    def load_delayed_packages(package_table, truck):
        all_packages = package_table.iterate_packages()
        delayed_packages = Helpers.filter_packages_by_status(all_packages, "delayed")
        for package in delayed_packages:
            Helpers.load_delayed_package_on_truck(package, truck, package_table)

    @staticmethod
    def get_package_distance(destination_address, current_address, address_list, distance_matrix):
        current_address_index = 0
        destination_index = 0
        for i, address in enumerate(address_list):
            if current_address in address.get_address():
                current_address_index = i
            if destination_address in address.get_address():
                destination_index = i
        distance = distance_matrix[current_address_index][destination_index]
        if distance == "":
            distance = distance_matrix[destination_index][current_address_index]
        distance = distance.replace('ï»¿', '')
        return float(distance)

    @staticmethod
    def get_packages_with_distance(packages, current_address, address_list, distance_matrix):
        packages_with_distance = [(package, Helpers.get_package_distance(package.get_address(), current_address, address_list, distance_matrix)) for package in packages]
        return packages_with_distance

    @staticmethod
    def sort_packages_by_distance(packages_with_distance):
        sorted_packages = sorted(packages_with_distance, key=lambda package:package[1])
        package_objects = [package[0] for package in sorted_packages]
        return package_objects

    @staticmethod
    def load_trucks_by_distance(package_table, truck1, truck2, truck3, address_list, distance_matrix):
        all_packages = package_table.iterate_packages()
        packages_to_load = Helpers.filter_packages_by_status(all_packages, "at the hub")
        packages_with_distance = Helpers.get_packages_with_distance(packages_to_load, "HUB", address_list, distance_matrix)
        sorted_package_values = Helpers.sort_packages_by_distance(packages_with_distance)

        for package_value in sorted_package_values:
            if truck1.get_available_capacity() > 0:
                Helpers.load_package_on_truck(package_value, truck1, package_table)
            elif truck2.get_available_capacity() > 0:
                Helpers.load_package_on_truck(package_value, truck2, package_table)
            elif truck3.get_available_capacity() > 0:
                Helpers.load_package_on_truck(package_value, truck3, package_table)

    @staticmethod
    def load_trucks(package_table, truck1, truck2, truck3, address_list, distance_matrix):
        Helpers.load_trucks_by_affinity(package_table, truck1, truck2, truck3)
        Helpers.load_trucks_by_EOD(package_table, truck1, truck2, truck3)
        Helpers.load_trucks_by_distance(package_table, truck1, truck2, truck3, address_list, distance_matrix)

    @staticmethod
    def get_nearest_package_id(current_address, undelivered_package_ids, package_table, address_list, distance_matrix):
        min_distance = 999999
        min_package_id = None
        for package_id in undelivered_package_ids:
            package = package_table.get_package(package_id)
            distance = Helpers.get_package_distance(package.get_address(), current_address, address_list, distance_matrix)
            if min_distance > distance:
                min_distance = distance
                min_package_id = package_id
        return [min_package_id, min_distance]

    @staticmethod
    def deliver_packages(package_table, truck, address_list, distance_matrix):
        while len(truck.get_package_ids()) > 0:
            current_address = truck.get_current_address()
            undelivered_package_ids = truck.get_package_ids()
            [nearest_package, distance] = Helpers.get_nearest_package_id(current_address, undelivered_package_ids, package_table, address_list, distance_matrix)
            package = package_table.get_package(nearest_package)
            truck.add_mileage_timestamp(truck.get_last_recorded_time() + datetime.timedelta(hours=distance/18), distance)
            # truck.set_last_recorded_time(truck.get_last_recorded_time() + datetime.timedelta(hours=distance/18))
            # truck.set_miles(truck.get_miles() + distance)
            truck.set_current_address(package.get_address())
            truck.deliver_package(nearest_package)
            package.set_delivery_status("delivered")
            package.set_delivery_time(truck.get_last_recorded_time())
        distance_to_hub = Helpers.get_package_distance("HUB", truck.get_current_address(), address_list, distance_matrix)
        # truck.set_last_recorded_time(truck.get_last_recorded_time() + datetime.timedelta(hours=distance_to_hub/18))
        # truck.set_miles(truck.get_miles() + distance_to_hub)
        truck.add_mileage_timestamp(truck.get_last_recorded_time() + datetime.timedelta(hours=distance_to_hub/18), distance_to_hub)
        truck.set_current_address("HUB")