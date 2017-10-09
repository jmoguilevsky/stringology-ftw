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
        occur = findAllOccurrences(text, SA, 'Jesus')
        for oc in occur:
            print()
            print(text[oc - 50: oc + 50])
            print()
        # def local2():
        # time = timeit(local2, number=1)
        # print('all occurrences', time)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
