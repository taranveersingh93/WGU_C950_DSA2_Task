from CSVReader import CSVReader
from HashTable import HashTable
from Helpers import Helpers
from Truck import Truck

packageTable = HashTable()

addressList = CSVReader.loadAddresses("./addresses.csv")
distanceMatrix = CSVReader.loadDistances("./distances.csv")
CSVReader.loadPackages("./packages.csv", packageTable)

truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)

Helpers.loadTrucks(packageTable, truck1, truck2, truck3)
print(truck1.capacity)
print(truck2.capacity)
print(truck3.capacity)