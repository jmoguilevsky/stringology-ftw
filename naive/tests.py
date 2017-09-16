import unittest
from .naive import naiveFind

class TestStringMethods(unittest.TestCase):

    def test_shortertext(self):
        self.assertEqual(naiveFind('hola', 'hol'), False)

    def test_equalTexts(self):
        self.assertEqual(naiveFind('hola', 'hola'), True)

    def test_textAtStart(self):
        self.assertEqual(naiveFind('hola', 'holaA'), True)

    def test_textAtMiddle(self):
        self.assertEqual(naiveFind('hola', 'AholaA'), True)

    def test_textAtTheEnd(self):
        self.assertEqual(naiveFind('hola', 'Ahola'), True)

    def test_textIsntThere(self):
        self.assertEqual(naiveFind('hola', 'AholAa'), False)

if __name__ == '__main__':
    unittest.main()