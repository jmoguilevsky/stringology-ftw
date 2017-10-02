import unittest
from dc3 import radix_pass


class TestRadix(unittest.TestCase):

    def test_banana(self):
        a = [1, 2, 4, 5, 7]
        b = [0, 0, 0, 0, 0]
        s = [2, 1, 3, 1, 3, 1, 0, 0, 0, 0]
        offset = 2
        N = 5
        K = 3
        radix_pass(a, b, s, offset, N, K)
        self.assertEqual(b, [4, 5, 7, 1, 2])

    def test_banana2(self):
        a = [1, 2, 4, 5]
        b = [0, 0, 0, 0]
        s = [2, 1, 3, 1, 3, 1, 0, 0, 0]
        offset = 2
        N = 4
        K = 3
        radix_pass(a, b, s, offset, N, K)
        self.assertEqual(b, [4, 5, 1, 2])

    def test_banana3(self):
        a = [4, 5, 1, 2]
        b = [0, 0, 0, 0]
        s = [2, 1, 3, 1, 3, 1, 0, 0, 0]
        offset = 1
        N = 4
        K = 3
        radix_pass(a, b, s, offset, N, K)
        self.assertEqual(b, [5, 4, 2, 1])

    def test_banana4(self):
        a = [5, 4, 2, 1]
        b = [0, 0, 0, 0]
        s = [2, 1, 3, 1, 3, 1, 0, 0, 0]
        offset = 0
        N = 4
        K = 3
        radix_pass(a, b, s, offset, N, K)
        self.assertEqual(b, [5, 1, 4, 2])

    def test_banana5(self):
        a = [0, 3]
        b = [0, 0]
        s = [2, 1, 3, 1, 3, 1, 0, 0, 0]
        offset = 0
        N = 2
        K = 3
        radix_pass(a, b, s, offset, N, K)
        self.assertEqual(b, [3, 0])

    def test_mississippi(self):
        a = [1, 2, 4, 5, 7, 8, 10]
        b = [0] * len(a)
        s = [2, 1, 4, 4, 1, 4, 4, 1, 3, 3, 1, 0, 0, 0]
        offset = 2
        N = 7
        K = 4
        radix_pass(a, b, s, offset, N, K)
        self.assertEqual(b, [10, 2, 5, 8, 7, 1, 4])

    def test_mississippi2(self):
        a = [10, 2, 5, 8, 7, 1, 4]
        b = [0] * len(a)
        s = [2, 1, 4, 4, 1, 4, 4, 1, 3, 3, 1, 0, 0, 0]
        offset = 1
        N = 7
        K = 4
        radix_pass(a, b, s, offset, N, K)
        self.assertEqual(b, [10, 8, 7, 2, 5, 1, 4])

    def test_mississippi3(self):
        a = [10, 8, 7, 2, 5, 1, 4]
        b = [0] * len(a)
        s = [2, 1, 4, 4, 1, 4, 4, 1, 3, 3, 1, 0, 0, 0]
        offset = 0
        N = 7
        K = 4
        radix_pass(a, b, s, offset, N, K)
        self.assertEqual(b, [10, 7, 1, 4, 8, 2, 5])

    def test_mississippi4(self):
        a = [1, 2, 4, 5, 7]
        b = [0] * len(a)
        s = [3, 3, 2, 1, 5, 5, 4, 0, 0, 0]
        offset = 2
        N = 5
        K = 5
        radix_pass(a, b, s, offset, N, K)
        self.assertEqual(b, [5, 7, 1, 4, 2])


if __name__ == '__main__':
    unittest.main()
