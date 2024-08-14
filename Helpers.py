
class Helpers:
    @staticmethod
    def loadPackageOnTruck(packageValue, truck, packageTable):
        if packageValue.deliveryStatus == "at the hub":
            truck.packages.append(packageValue)
            truck.capacity = truck.capacity - 1
            package = packageTable.get_package(packageValue.getId())
            package.set_deliveryStatus("loaded")
            packageTable.set_package(package.getId(), package)

    @staticmethod
    def loadTrucksByAffinity(packageTable, truck1, truck2, truck3):
        allPackages = packageTable.iterate_packages()
        for package in allPackages:
            if truck1.capacity > 0 and package.get_deliveryStatus() == "at the hub" and package.get_truckAffinity() == str(truck1.getId()):
                Helpers.loadPackageOnTruck(package, truck1, packageTable)
            elif truck2.capacity > 0 and package.get_deliveryStatus() == "at the hub" and package.get_truckAffinity() == str(truck2.getId()):
                Helpers.loadPackageOnTruck(package, truck2, packageTable)
            elif truck3.capacity > 0 and package.get_deliveryStatus() == "at the hub" and package.get_truckAffinity() == str(truck3.getId()):
                Helpers.loadPackageOnTruck(package, truck3, packageTable)

    @staticmethod
    def loadTrucksWithEOD(packageTable, truck1, truck2, truck3):
        allPackages = packageTable.iterate_packages()
        for package in allPackages:
            if package.deadline == "EOD":
                if truck3.capacity > 0 and package.get_deliveryStatus() == "at the hub":
                    Helpers.loadPackageOnTruck(package, truck3, packageTable)
                elif truck2.capacity > 0 and package.get_deliveryStatus() == "at the hub":
                    Helpers.loadPackageOnTruck(package, truck2, packageTable)
                elif truck1.capacity > 0 and package.get_deliveryStatus() == "at the hub":
                    Helpers.loadPackageOnTruck(package, truck1, packageTable)
    @staticmethod
    def filterPackagesByStatus(packages, status):
        packagesWithStatus = [package for package in packages if package.deliveryStatus == status]
        return packagesWithStatus

    @staticmethod
    def getPackageDistance(package, currentLocation, addressList, distanceMatrix):
        currentLocationIndex = 0
        destinationIndex = 0
        for i, address in enumerate(addressList):
            if currentLocation in address.get_address():
                currentLocationIndex = i
            if package.get_address() in address.get_address():
                destinationIndex = i
        distance = distanceMatrix[currentLocationIndex][destinationIndex]
        if distance == "":
            distance = distanceMatrix[destinationIndex][currentLocationIndex]
        return float(distance)

    @staticmethod
    def getPackagesWithDistances(packages, currentLocation, addressList, distanceMatrix):
        packagesWithDistance = [(package, Helpers.getPackageDistance(package, currentLocation, addressList, distanceMatrix)) for package in packages]
        return packagesWithDistance

    @staticmethod
    def sortPackagesByDistance(packagesWithDistance):
        sortedPackages = sorted(packagesWithDistance, key=lambda package:package[1])
        packageObjects = [package[0] for package in sortedPackages]
        return packageObjects

    @staticmethod
    def loadTrucksByDistance(packageTable, truck1, truck2, truck3, addressList, distanceMatrix):
        allPackages = packageTable.iterate_packages()
        packagesToLoad = Helpers.filterPackagesByStatus(allPackages, "at the hub")
        packagesWithDistance = Helpers.getPackagesWithDistances(packagesToLoad, "HUB", addressList, distanceMatrix)
        sortedPackagesByDistance = Helpers.sortPackagesByDistance(packagesWithDistance)

        for packageValue in sortedPackagesByDistance:
            if truck1.capacity > 0:
                Helpers.loadPackageOnTruck(packageValue, truck1, packageTable)
            elif truck2.capacity > 0:
                Helpers.loadPackageOnTruck(packageValue, truck2, packageTable)
            elif truck3.capacity > 0:
                Helpers.loadPackageOnTruck(packageValue, truck3, packageTable)

    @staticmethod
    def loadTrucks(packageTable, truck1, truck2, truck3, addressList, distanceMatrix):
        Helpers.loadTrucksByAffinity(packageTable, truck1, truck2, truck3)
        Helpers.loadTrucksWithEOD(packageTable, truck1, truck2, truck3)
        Helpers.loadTrucksByDistance(packageTable, truck1, truck2, truck3, addressList, distanceMatrix)
