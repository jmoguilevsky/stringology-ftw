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

        def searcher(name):
            def local():
                findAllOccurrences(text, SA, name)
                # print(name, len(findAllOccurrences(text, SA, name)))
            return local
        funs = []
        for n in names:
            f = searcher(n)
            # print('occurrences', n, f())
            times = 1000
            time = timeit(f, number=times)
            print(n, time/times)

        # for f in funs:
        #     print(f)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
