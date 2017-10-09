import unittest
from timeit import timeit
from os import listdir
from os.path import isfile, join, getsize
from dc3 import radix_pass, naively_suffix_array, suffix_array
from applications import findAllOccurrences


class TestApplications(unittest.TestCase):

    def test_in_bible(self):
        f = open('../texts/bible.txt', 'r')
        text = f.read()
        f.close()
        SA = suffix_array(text)
        names = ['God', 'Jesus', 'Peter', 'Moses', ' and ', 'Leah', 'ASDG']
        # names = ['God', 'Moses', 'Zam', 'zum']
        def searcher(name):
            def local():
                left, right = findAllOccurrences(text, SA, name)
                print(name, right - left)
            return local

        for n in names:
            times = 1
            time = timeit(searcher(n), number=times)
            print(n, time/times)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
