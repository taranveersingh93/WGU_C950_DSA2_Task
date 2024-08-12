class HashTable:
    def __init__(self, size=11):
        self.data_map = [None] * size

    def __hash(self, key):
        my_hash = 0
        for character in key:
            my_hash = (my_hash + ord(character)*17)
        my_hash = my_hash % len(self.data_map)
        return my_hash

    def set_package(self, key, value):
        index = self.__hash(key)
        if (self.data_map[index] == None):
            self.data_map[index] = []
        self.data_map[index].append([key, value])

    def get_item(self, key):
        index = self.__hash(key)
        if self.data_map[index] is not None:
            for package in self.data_map[index]:
                if package[0] == key:
                    return package[1]
        return None