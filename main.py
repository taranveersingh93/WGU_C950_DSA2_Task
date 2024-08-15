import datetime

from CSVReader import CSVReader
from HashTable import HashTable
from Helpers import Helpers
from Truck import Truck

package_table = HashTable()

address_list = CSVReader.load_addresses("./addresses.csv")
distance_matrix = CSVReader.load_distances("./distances.csv")
CSVReader.load_packages("./packages.csv", package_table)

truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)

Helpers.load_trucks(package_table, truck1, truck2, truck3, address_list, distance_matrix)
truck1.set_departure_time(datetime.timedelta(hours=8))
truck2.set_departure_time(datetime.timedelta(hours=9, minutes=5))

Helpers.deliver_packages(package_table, truck1, address_list, distance_matrix)
Helpers.load_delayed_packages(package_table, truck2)
Helpers.deliver_packages(package_table, truck2, address_list, distance_matrix)
package_9 = package_table.get_package("9")
package_9.set_address("410 S. State St., Salt Lake City, UT 84111")
package_table.set_package("9", package_9)
driver_availability_time = min(truck1.get_last_recorded_time(), truck2.get_last_recorded_time())
address_change_time = datetime.timedelta(hours=10, minutes=20)
truck3.set_departure_time(max(address_change_time, driver_availability_time))
Helpers.deliver_packages(package_table, truck3, address_list, distance_matrix)

class Main:
    print("WGUPS Delivery Tracking")
    print(f"The total mileage: {truck1.get_miles() + truck2.get_miles() + truck3.get_miles()}")
    print("="*20)
    user_time = input("Enter the time of day in format 'HH:MM' at which you want to check the status: ")
    (input_h, input_m) = user_time.split(":")
    try:
        check_time = datetime.timedelta(hours=int(input_h), minutes=int(input_m))
        print("1. View status of all packages.")
        print("2. View status of a single package.")
        user_option = input("Input the number corresponding to your option and press enter: ")
        try:
            if (user_option == "1"):
                all_packages = package_table.iterate_packages()
                for package in all_packages:
                    departure_time = None
                    if (package.get_truck_id() == 1):
                        departure_time = truck1.get_departure_time()
                    elif (package.get_truck_id() == 2):
                        departure_time = truck2.get_departure_time()
                    else:
                        departure_time = truck3.get_departure_time()
                    print(package.get_status(check_time, departure_time))
                    print("-"*10)
            elif (user_option == "2"):
                print("=" * 20)
                secondInput = input("Input the package ID (1-40) and press enter: ")
                try:
                    if int(secondInput) > 40 or int(secondInput) < 1:
                        print("Invalid input")
                    else:
                        print("-" * 10)
                        package = package_table.get_package(secondInput)
                        departure_time = None
                        if (package.get_truck_id() == 1):
                            departure_time = truck1.get_departure_time()
                        elif (package.get_truck_id() == 2):
                            departure_time = truck2.get_departure_time()
                        else:
                            departure_time = truck3.get_departure_time()
                        print(package.get_status(check_time, departure_time))
                        print("-" * 10)
                except ValueError:
                    print("Invalid input")
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")
    except ValueError:
        print("Invalid input")



# print(truck1.get_last_recorded_time())
# print(truck1.get_miles())
# print(truck1.get_package_ids())
#
# print(truck2.get_last_recorded_time())
# print(truck2.get_miles())
# print(truck2.get_package_ids())
# all_packages = package_table.iterate_packages()
# print(truck3.get_last_recorded_time())
# print(truck3.get_departure_time())
# print(truck3.get_miles())
# print(truck3.get_package_ids())
