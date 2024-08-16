# WGUPS by Taranveer Singh
# Student ID: 011834733

import datetime

from CSVReader import CSVReader
from HashTable import HashTable
from Helpers import Helpers
from Truck import Truck

# initialize a hashtable
package_table = HashTable()

#store the csv data to relevant variables
address_list = CSVReader.load_addresses("./addresses.csv")
distance_matrix = CSVReader.load_distances("./distances.csv")
CSVReader.load_packages("./packages.csv", package_table)

# initialize the trucks and store them in an array
truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)
trucks = [truck1, truck2, truck3]

# load the trucks
Helpers.load_trucks(package_table, truck1, truck2, truck3, address_list, distance_matrix)

# set truck 1's departure time to the earliest possible 08:00
truck1.set_departure_time(datetime.timedelta(hours=8))
# set truck 2's departure time to 09:05 so that it leaves as soon as the delayed packages arrive
truck2.set_departure_time(datetime.timedelta(hours=9, minutes=5))

# have the truck1 deliver its packages
Helpers.deliver_packages(package_table, truck1, address_list, distance_matrix)

# load the delayed packages on truck 2
Helpers.load_delayed_packages(package_table, truck2)

# have the truck2 deliver its packages
Helpers.deliver_packages(package_table, truck2, address_list, distance_matrix)

# initialize package 9 to update its address.
package_9 = package_table.get_package("9")
package_9.set_address("410 S. State St., Salt Lake City, UT 84111")
# update the package table's package 9
package_table.set_package("9", package_9)
# since there are only 2 drivers available, truck 3 can't leave before the earliest truck returns.
driver_availability_time = min(truck1.get_last_recorded_time(), truck2.get_last_recorded_time())
address_change_time = datetime.timedelta(hours=10, minutes=20)
# truck 3 also can't leave until the addres has been changed. It can only leave at the later of the two times.
truck3.set_departure_time(max(address_change_time, driver_availability_time))
# have the truck 3 deliver its packages
Helpers.deliver_packages(package_table, truck3, address_list, distance_matrix)

class Main:
    print("WGUPS Delivery Tracking")
    print(f"The total mileage: {truck1.get_final_mileage() + truck2.get_final_mileage() + truck3.get_final_mileage()}")
    print("="*20)
    user_time = input("Enter the time of day in format 'HH:MM' at which you want to check the status: ")
    # split the user input by ":" and store them in different variables
    (input_h, input_m) = user_time.split(":")
    try:
        check_time = datetime.timedelta(hours=int(input_h), minutes=int(input_m))
        print("="*10)
        # list initial options
        print("1. View status of all packages.")
        print("2. View status of a single package.")
        print("3. View status of packages by truck.")
        print("4. View packages by status.")
        print("5. View total mileage at the entered time")

        # ask for the user to select what they want to do
        user_option = input("Input the number corresponding to your option(1-5) and press enter: ")
        try:
            if user_option == "1":
                # get all packages
                all_packages = package_table.get_all_packages()
                print("-"*20)
                # loop through the packages and print each package's status
                for package in all_packages:
                    truck_id = package.get_truck_id()
                    truck = trucks[truck_id-1]
                    departure_time = truck.get_departure_time()
                    print(package.get_status(check_time, departure_time))
                print("-"*20)
            elif user_option == "2":
                print("=" * 20)
                # ask for a package id
                secondInput = input("Input the package ID (1-40) and press enter: ")
                try:
                    # basic error handling for a non existent package id
                    if int(secondInput) > 40 or int(secondInput) < 1:
                        print("Invalid input")
                    else:
                        print("-" * 10)
                        package = package_table.get_package(secondInput)
                        departure_time = None
                        # departure time can only be found from the truck.
                        if (package.get_truck_id() == 1):
                            departure_time = truck1.get_departure_time()
                        elif (package.get_truck_id() == 2):
                            departure_time = truck2.get_departure_time()
                        else:
                            departure_time = truck3.get_departure_time()
                        # use departure time and the query time entered by user to call package's status method
                        print(package.get_status(check_time, departure_time))
                        print("-" * 10)
                except ValueError:
                    print("Invalid input")
            elif user_option == "3":
                try:
                    truck_number = input("Input the truck ID (1-3) and press enter: ")
                    truck = trucks[int(truck_number) - 1]
                    undelivered_packages = truck.get_package_ids()
                    delivered_packages = truck.get_delivered_package_ids()
                    # use destructuring to combine the arrays
                    all_packages = [*undelivered_packages, *delivered_packages]
                    departure_time = truck.get_departure_time()
                    print("-" * 10)
                    # loop through the packages to print the status
                    for package_id in all_packages:
                        package = package_table.get_package(package_id)
                        print(package.get_status(check_time, departure_time))
                        print("-" * 10)

                except ValueError:
                    print("Invalid input")
            elif user_option == "4":
                status_options = ["Delayed", "Loaded", "On its way", "Delivered"]
                # print all status_options
                for i, status in enumerate(status_options):
                    print(f"{i+1}: {status}")
                # record user input
                status_option = input("Input the number corresponding to your option(1-4) and press enter: ")
                try:
                    status_choice = status_options[int(status_option) - 1]
                    all_packages = package_table.get_all_packages()
                    # get packages filtered by status IN HINDSIGHT using a query time (check_time)
                    filtered_packages = Helpers.filter_packages_by_status_with_time(all_packages, status_choice, check_time, trucks)
                    print("-" * 10)
                    # loop through the filtered packages to print their status
                    for package in filtered_packages:
                        truck_id = package.get_truck_id()
                        truck = trucks[truck_id - 1]
                        departure_time = truck.get_departure_time()
                        print(package.get_status(check_time, departure_time))
                        print("-" * 10)
                except ValueError:
                    print("Invalid input")
            elif user_option == "5":
                print("-" * 10)
                print("Mileage at EOD:")
                print(f"Total Mileage: {truck1.get_final_mileage() + truck2.get_final_mileage() + truck3.get_final_mileage()}")
                print(f"Truck 1: {truck1.get_final_mileage()}")
                print(f"Truck 2: {truck2.get_final_mileage()}")
                print(f"Truck 3: {truck3.get_final_mileage()}")
                print("-"*10)
                print(f"Mileage as of {check_time}:")
                print(f"Total Mileage: {truck1.get_mileage_at(check_time) + truck2.get_mileage_at(check_time) + truck3.get_mileage_at(check_time)}")
                print(f"Truck 1: {truck1.get_mileage_at(check_time)}")
                print(f"Truck 2: {truck2.get_mileage_at(check_time)}")
                print(f"Truck 3: {truck3.get_mileage_at(check_time)}")
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")
    except ValueError:
        print("Invalid input")