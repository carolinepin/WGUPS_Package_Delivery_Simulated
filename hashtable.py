import packages

class HashTable:
    def __init__(self, size):
        self.__size = size
        self.__buckets = [None] * self.__size

    # Runtime complexity of O(1)
    def get_size(self):
        return self.__size

    # Runtime complexity of O(1)
    #takes package id and hashes it
    def get_hash(self, key):
        #hash = key**2 + key**3    #might not work
        hash = (key+100) % self.__size    #so it can never exceed the max size of array
        #hashed = key%hash
        #print(f'the key ', {key+100}, ' gets hashed into ', {hash})
        return hash

    # Runtime complexity of O(1)
    # takes package and put it in hash table
    def hashInsert(self, key, value):
        key_hash = self.get_hash(key)
        key_value = [key, value]

        #chaining
        if self.__buckets[key_hash] is None:
            self.__buckets[key_hash] = list([key_value])
            return True
        else:
            for pair in self.__buckets[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.__buckets[key_hash].append(key_value)
            return True

    # Runtime complexity of O(1)
    # receives package id and returns the matching package object
    def lookup(self, key):
        key_hash = self.get_hash(key)
        if self.__buckets[key_hash] is None:
            return None
        else:
            for pair in self.__buckets[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Runtime complexity of O(n)
    # this function is for debugging, thus I will not optimize it to take into account that a bucket can have more\
    # than one value in it. in the future I hope to find a way to optimize it to print all items in bucket
    def printWholeHashTable(self):
        print("HASH TABLE INFO")
        for item in self.__buckets:
            if item is not None:
                print(f'{item[0][1]}\n')