class HashTable:
    def __init__(self, size=11):
        # initialize the table with a list of size 11 and each value None.
        # a size of prime number helps reduce collisions.
        self.data_map = [None] * size

    def __hash(self, key):
        # private method to compute a hash value for a key
        my_hash = 0
        # go through the characters
        for character in key:
            # Add the ASCII equivalent x 17 to the my_hash value.
            my_hash = (my_hash + ord(character)*17)
        # after the for loop, use modulo to ensure that the hash value fits the array size
        my_hash = my_hash % len(self.data_map)
        return my_hash

    def set_package(self, key, value):
        # get the hash value for the key. This gives the index in data_map.
        # It will act as a "slot" for single/multiple packages.
        index = self.__hash(key)

        # if the slot is empty, initialize an empty array there.
        if (self.data_map[index] == None):
            self.data_map[index] = []
        else:
            # otherwise, loop through the existing array
            for package in self.data_map[index]:
                # if a matching key is found, then this method updates the existing package and stops (returns)
                if package[0] == key:
                    package[1] = value
                    return
        # if the matching key is not found, then add the [key, package] to the list existing at the "slot"
        self.data_map[index].append([key, value])

    def get_package(self, key):
        # get the data_map index using the hash function on the key
        index = self.__hash(key)
        # if the slot is not empty
        if self.data_map[index] is not None:
            # loop through the array that exists in the slot
            for package in self.data_map[index]:
                # if a match is found for the key, return the package
                if package[0] == key:
                    return package[1]
        # return None if no match found.
        return None

    def get_all_packages(self):
        # initialize an empty list.
        packages = []
        # loop through the data map. Data map consists slots and slots consist of [key, package] arrays
        for slot in self.data_map:
            # if a slot exists, then it's an array
            if slot is not None:
                # loop through the package array in the slot
                for package in slot:
                    # add the package value, not the entire [key, package] to the packages array.
                    packages.append(package[1])
        return packages
