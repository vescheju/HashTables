"""
Implemented by: Yash Vesikar, Brandon Field and Justin Vesche
"""


class HashNode:
    """
    DO NOT EDIT
    """
    __slots__ = ["key", "value", "deleted"]

    def __init__(self, key, value, deleted=False):
        self.key = key
        self.value = value
        self.deleted = deleted

    def __repr__(self):
        return f"HashNode({self.key}, {self.value})"

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

    def __iadd__(self, other):
        self.value += other


class HashTable:
    """
    Hash Table Class
    """
    __slots__ = ['capacity', 'size', 'table', 'prime_index']

    primes = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
        89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
        281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
        619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
        743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991,
        997)

    def __init__(self, capacity=8):
        """
        DO NOT EDIT
        Initializes hash table
        :param capacity: capacity of the hash table
        """
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

        i = 0
        while HashTable.primes[i] <= self.capacity:
            i += 1
        self.prime_index = i - 1

    def __eq__(self, other):
        """
        DO NOT EDIT
        Equality operator
        :param other: other hash table we are comparing with this one
        :return: bool if equal or not
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False
        for i in range(self.capacity):
            if self.table[i] != other.table[i]:
                return False
        return True

    def __repr__(self):
        """
        DO NOT EDIT
        Represents the table as a string
        :return: string representation of the hash table
        """
        represent = ""
        bin_no = 0
        for item in self.table:
            represent += "[" + str(bin_no) + "]: " + str(item) + '\n'
            bin_no += 1
        return represent

    def _hash_1(self, key):
        """
        ---DO NOT EDIT---
        Converts a string x into a bin number for our hash table
        :param key: key to be hashed
        :return: bin number to insert hash item at in our table, None if key is an empty string
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)
        return hashed_value % self.capacity

    def _hash_2(self, key):
        """
        ---DO NOT EDIT---
        Converts a string x into a hash
        :param x: key to be hashed
        :return: a hashed value
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        prime = HashTable.primes[self.prime_index]

        hashed_value = prime - (hashed_value % prime)
        if hashed_value % 2 == 0:
            hashed_value += 1
        return hashed_value

    def __len__(self):
        """
        don't edit this plz
        Getter for size
        :return: size
        """
        return self.size

    ########## EDIT BELOW ##########

    def __setitem__(self, key, value):
        """
        Inserts into the hash
        :return: None
        """
        self._insert(key, value)

    def __getitem__(self, key):
        """
        gets the item given the key in hash
        :return: the value
        """
        found = self._get(key)
        if found is None:
            raise KeyError
        return found.value

    def __delitem__(self, key):
        """
        deletes an item given a key
        :return: None
        """
        found = self.hash(key)
        if self.table[found] is None:
            raise KeyError
        self._delete(key)

    def __contains__(self, key):
        """
        finds if a key exists in the hash
        :return: bool
        """
        found = self.hash(key)
        if self.table[found] is None:
            return False
        return True

    def hash(self, key, inserting=False):
        """
        uses a double hash method to either find an index of where to insert, or to find a given key.
        :return: Depends on inserting, could be None, where a value is deleted, or where key was already.
        """
        i = 0
        double_hashed = self._hash_1(key) + i*self._hash_2(key)
        double_hashed = double_hashed % self.capacity
        while True:
            if inserting:
                if self.table[double_hashed] is None or self.table[double_hashed].deleted:
                    return double_hashed
                elif self.table[double_hashed].key == key:
                    return double_hashed
            else:
                if self.table[double_hashed] is None:
                    return double_hashed
                elif self.table[double_hashed].key == key:
                    return double_hashed
            i += 1
            double_hashed = self._hash_1(key) + i * self._hash_2(key)
            double_hashed = double_hashed % self.capacity


    def _insert(self, key, value):
        """
        Inserts into the hash, calls grow if needed
        :return: None
        """
        found = self.hash(key, True)
        if self.table[found] is None or self.table[found].deleted:
            node = HashNode(key, value)
            self.table[found] = node
            self.size += 1
            if self.size >= self.capacity // 2:
                self.size = 0
                self._grow()
        else:
            self.table[found].value = value

    def _get(self, key):
        """
        get the node given a key
        :return: None or a node
        """
        found = self.hash(key)
        if self.table[found] is None:
            return None
        return self.table[found]

    def _delete(self, key):
        """
        changes a node key and value to none, also sets deleted to true
        :return: None
        """
        found = self.hash(key)
        if self.table[found] is not None:
            self.table[found].key = None
            self.table[found].value = None
            self.table[found].deleted = True
            self.size -= 1

    def _grow(self):
        """
        Increase the capacity of the hash table, rehashing each value in the list
        :return: None
        """
        old_size = self.capacity
        new_size = self.capacity * 2
        self.capacity = new_size
        i = 0
        while HashTable.primes[i] <= new_size:
            i += 1
        self.prime_index = i - 1
        new_array = [None] * new_size
        old_array = self.table
        self.table = new_array
        index = 0
        while index < old_size:
            if old_array[index] is not None:
                if not old_array[index].deleted:
                    node = old_array[index]
                    self._insert(node.key, node.value)
            index += 1


    def update(self, pairs=[]):
        """
        Update the hashtable given a pair, if key is not in the table insert it.
        :return: None
        """
        for i in pairs:
            self._insert(i[0], i[1])

    def setdefault(self, key, default=None):
        """
        Find a key and return its value, if its not in the hash table insert it.
        :return: default or the found value
        """
        found = self.hash(key)
        if self.table[found] is None or self.table[found].deleted:
            self._insert(key, default)
            return default
        else:
            return self.table[found].value

    def keys(self):
        """
        Create a generator object of the keys in the list
        :return: None
        """
        for i in self.table:
            if i is not None and not i.deleted:
                yield i.key

    def values(self):
        """
        Create a generator object of the values in the list
        :return: None
        """
        for i in self.table:
            if i is not None and not i.deleted:
                yield i.value


    def items(self):
        """
        Create a generator object of the keys and values in the list
        :return: None
        """
        for i in self.table:
            if i is not None and not i.deleted:
                yield (i.key, i.value)

    def clear(self):
        """
        Clear all values in the hash table
        :return: None
        """
        i = 0
        while i < self.capacity:
            self.table[i] = None
            i += 1
        self.size = 0

def hurdles(grid):
    table = HashTable()
    if len(grid) == 1:
        if len(grid[0]) > 1:
            return 0
        return 1
    for row in grid:
        len_row = 0
        for path in row[0:-1]:
            len_row += path
            key = str(len_row)
            found = table.hash(key, True)
            if table.table[found] is not None and table.table[found].key == key:
                value = table[key]
                value += 1
                table[key] = value
            else:
                table[key] = 1
    max_hurd = 0
    # Find the Max number of junctions in the single path
    for i in table.table:
        if i is not None:
            if max_hurd == 0:
                max_hurd = i.value
            elif max_hurd < i.value:
                max_hurd = i.value
    return len(grid) - max_hurd









