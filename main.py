from CSVReader import CSVReader
from HashTable import HashTable
from Helpers import Helpers
from Truck import Truck

package_table = HashTable()

addressList = CSVReader.load_addresses("./addresses.csv")
distanceMatrix = CSVReader.load_distances("./distances.csv")
CSVReader.load_packages("./packages.csv", package_table)

truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)

Helpers.load_trucks(package_table, truck1, truck2, truck3, addressList, distanceMatrix)
print(truck1.get_available_capacity())
print(truck2.get_available_capacity())
print(truck3.get_available_capacity())