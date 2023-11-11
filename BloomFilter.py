"""
BloomFilter.py

This script contains the implementation of a Bloom filter class.

The BloomFilter class has the following methods:
- __init__(self, n, fp_rate): Initializes the BloomFilter object with the given number of items (n) and false positive rate (fp_rate).
- hash_func_fact(self, m): Returns a hash function that hashes an input (x) into one of the m array positions.
- insert(self, key): Inserts a key into the Bloom filter.

The BloomFilter class uses the following external libraries:
- math: Provides access to mathematical functions.
- random: Provides functions for generating random numbers.
- bitarray: Provides an object type that efficiently represents an array of booleans.
- sklearn.utils: Provides utility functions, including murmurhash3_32 for hashing.

Author: Daniel Li, Ben Leebron
Date: 11/8/2023
"""

import math
import random
from bitarray import bitarray
from sklearn.utils import murmurhash3_32

class BloomFilter():
    def __init__(self, n, fp_rate):
        self.n = n
        self.fp_rate = fp_rate
        # find r
        self.r = int(math.log(fp_rate, 0.618) * n)
        self.bit_array = self.r * bitarray('0')
        self.k = int(self.r / self.n * math.log(2, math.e))
        # we reference this list to call each of the k hash functions
        self.hash_functions = [self.hash_func_fact(self.r) for i in range(self.k)]

    def hash_func_fact(self, m):
        """
        Returns a hash function that maps a string to an integer in the range [0, m).
        
        Args:
        - m (int): The range of the hash function.
        
        Returns:
        - hash_func (function): A hash function that maps a string to an integer in the range [0, m).
        """
        seed = random.randrange(0,1024)
        def hash_func(x):
            return murmurhash3_32(x, seed=seed) % m
        return hash_func
  
    def insert(self, key):
        """
        Inserts a key into the Bloom filter by setting the bits at the positions
        returned by the hash functions to 1.

        Args:
            key: The key to insert into the Bloom filter.

        Returns:
            None
        """
        for hf in self.hash_functions:
            self.bit_array[hf(key)] = 1

  # if we encounteer a single 0, return false.
    def test(self, key):
        """
        Check if a given key is probably in the set represented by the Bloom filter.

        Args:
            key: The key to check.

        Returns:
            True if the key is probably in the set, False otherwise.
        """
        for hf in self.hash_functions:
            if self.bit_array[hf(key)] == 0:
                return False            
        return True

