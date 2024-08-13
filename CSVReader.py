import csv

from Address import Address
from Package import Package


class CSVReader:
    @staticmethod
    def loadAddresses(fileName):
        addressList = []
        with open(fileName) as addresses:
            addressData = csv.reader(addresses, delimiter=',')
            next(addressData) #skip header
            for row in addressData:
                address = Address(row[0], row[1])
                addressList.append(address)
        return addressList

    @staticmethod
    def loadPackages(fileName, hashTable):
        packageList = []
        with open(fileName) as packages:
            packageData = csv.reader(packages, delimiter=',')
            next(packageData)
            for row in packageData:
                packageId = row[0]
                packageDestination = row[1]
                packageCity = row[2]
                packageZip = row[4]
                packageDeadline = row[5]
                packageWeight = int(row[6])
                packageNote = row[7]
                packageTruckAffinity = row[8]
                packageDevliveryStatus = "at the hub"

                if "Delayed" in packageNote:
                    packageDevliveryStatus = "delayed"

                package = Package(packageId, packageDestination, packageDeadline, packageCity, packageZip,packageWeight,packageDevliveryStatus, packageNote, packageTruckAffinity)
                packageList.append(package)
                # if packageTruckAffinity == "1" or packageTruckAffinity == "2" or packageTruckAffinity == "3":
                #     packageListWithAffinity.append(package)
                # else:
                #     packageListWithoutAffinity.append(package)
        for package in packageList:
            hashTable.set_package(package.getId(), package)
        # for package in packageListWithAffinity:
        #     hashTable.addPackage(package)
        # for package in packageListWithoutAffinity:
        #     hashTable.addPackage(package)

    @staticmethod
    def loadDistances(fileName):
        data = []
        with open(fileName) as distances:
            distanceData = csv.reader(distances, delimiter=',')
            data = list(distanceData)
        return data



