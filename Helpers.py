

class Helpers:
    @staticmethod
    def loadPackageOnTruck(packageValue, truck, packageTable):
        if packageValue.deliveryStatus == "at the hub":
            truck.packages.append(packageValue)
            truck.capacity = truck.capacity - 1
            package = packageTable.get_package(packageValue.getId())
            package[1].deliveryStatus = "loaded"
            packageTable.set_package(package)

    @staticmethod
    def loadTrucksByAffinity(packageTable, truck1, truck2, truck3):
        for package in packageTable:
            if truck1.capacity > 0 and package[1].deliveryStatus == "at the hub" and package[1].truckAffinity == str(truck1.truckId):
                Helpers.loadPackageOnTruck(package[1], truck1, packageTable)
            if truck2.capacity > 0 and package[1].deliveryStatus == "at the hub" and package[1].truckAffinity == str(truck2.truckId):
                Helpers.loadPackageOnTruck(package[1], truck2, packageTable)
            if truck3.capacity > 0 and package[1].deliveryStatus == "at the hub" and package[1].truckAffinity == str(truck3.truckId):
                Helpers.loadPackageOnTruck(package[1], truck3, packageTable)

    @staticmethod
    def loadTrucksWithEOD(packageTable, truck1, truck2, truck3):
        for package in packageTable:
            if package[1].packageDeadline == "EOD":
                if truck3.capacity > 0 and package[1].deliveryStatus == "at the hub":
                    Helpers.loadPackageOnTruck(package[1], truck3, packageTable)
                if truck2.capacity > 0 and package[1].deliveryStatus == "at the hub":
                    Helpers.loadPackageOnTruck(package[1], truck2, packageTable)
                if truck1.capacity > 0 and package[1].deliveryStatus == "at the hub":
                    Helpers.loadPackageOnTruck(package[1], truck1, packageTable)

    @staticmethod
    def filterPackagesByStatus(packages, status):
        packagesWithStatus = [package for package in packages if package.deliveryStatus == status]
        return packagesWithStatus

    @staticmethod
    def getPackageDistance(package, currentLocation, addressList, distanceMatrix):
        currentLocationIndex = 0
        destinationIndex = 0
        for i, address in enumerate(addressList):
            if address[1] == currentLocation:
                currentLocationIndex = i-1
            if address[1] == package.address:
                destinationIndex = i-1
        distance = distanceMatrix[currentLocationIndex][destinationIndex]
        if distance == "":
            distance = distanceMatrix[destinationIndex][currentLocationIndex]
        return distance



    @staticmethod
    def getPackagesWithDistances(packages, currentLocation):
        packagesWithDistance = [(package, Helpers.getPackageDistance(package, currentLocation, addressList, distanceMatrix)) for package in packages]
        return packagesWithDistance

    @staticmethod
    def sortPackagesByDistance(packagesWithDistance):
        sortedPackages = sorted(packagesWithDistance, key=lambda package:package[1])
        return sortedPackages

    @staticmethod
    def loadTrucksByDistance(packageTable, truck1, truck2, truck3):
        extractedPackageValues = list(packageTable.values())
        packagesToLoad = Helpers.filterPackagesByStatus(extractedPackageValues, "at the hub")
        packagesWithDistance = Helpers.getPackagesWithDistances(packagesToLoad, "HUB")
        sortedPackagesByDistance = Helpers.sortPackagesByDistance(packagesWithDistance)

        for packageValue in sortedPackagesByDistance:
            if truck1.capacity > 0:
                Helpers.loadPackageOnTruck(packageValue, truck1, packageTable)
            if truck2.capacity > 0:
                Helpers.loadPackageOnTruck(packageValue, truck2, packageTable)
            if truck3.capacity > 0:
                Helpers.loadPackageOnTruck(packageValue, truck3, packageTable)
