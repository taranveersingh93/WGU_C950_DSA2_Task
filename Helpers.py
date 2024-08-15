
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
        truck.packages.append(package_value)
        truck.set_reserved_capacity()(truck.get_reserved_capacity() - 1)
        package = package_table.get_package(package_value.get_id())
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
    def get_package_distance(package, current_location, address_list, distance_matrix):
        current_location_index = 0
        destination_index = 0
        for i, address in enumerate(address_list):
            if current_location in address.get_address():
                current_location_index = i
            if package.get_address() in address.get_address():
                destination_index = i
        distance = distance_matrix[current_location_index][destination_index]
        if distance == "":
            distance = distance_matrix[destination_index][current_location_index]
        return float(distance)

    @staticmethod
    def get_packages_with_distance(packages, current_location, address_list, distance_matrix):
        packages_with_distance = [(package, Helpers.get_package_distance(package, current_location, address_list, distance_matrix)) for package in packages]
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
