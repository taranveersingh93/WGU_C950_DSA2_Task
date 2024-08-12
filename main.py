from HashTable import HashTable

ht = HashTable()

# Adding some packages
ht.set_package("apple", ["this", "that", 20])
ht.set_package("banana", 20)
ht.set_package("orange", 30)

# Retrieving packages
print(ht.get_item("apple"))   # Should print 10
print(ht.get_item("banana"))  # Should print 20
print(ht.get_item("grape"))   # Should print None