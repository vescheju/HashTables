import unittest
from hashtable import HashTable, HashNode, hurdles


class TestProject1(unittest.TestCase):
    def test_hurdles(self):
        # input from picture in specs
        grid = [[1]]
        print(hurdles(grid))
        assert hurdles(grid) == 2

        grid = [[5, 2, 2, 1],
                [3, 2, 5],
                [1, 2, 1, 2, 1, 2, 1]]

        assert hurdles(grid) == 1


if __name__ == '__main__':
    unittest.main()
