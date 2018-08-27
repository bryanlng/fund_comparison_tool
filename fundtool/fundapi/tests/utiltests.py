import unittest
import sys

print("current sys path: ", sys.path)

from fundtool.fundapi.libraries import PerformanceStats

class UtilTests(unittest.TestCase):

    p = PerformanceStats()

    def testHappyPath(self):
        self.assertTrue(p.hasProperFormat("PRHSX"))

    def testHappyPathButNotAnActualSymbo(self):
        self.assertTrue(p.hasProperFormat("ZZZZZ"))

    def testContainsNumbers(self):
        self.assertFalse(p.hasProperFormat("334SX"))

    def testEmpty(self):
        self.assertFalse(p.hasProperFormat(""))

    def testNotLengthofFive(self):
        self.assertFalse(p.hasProperFormat("PRHX"))

    def testLowerCase(self):
        self.assertFalse(p.hasProperFormat("PRsHX"))

    def testGreaterLengthofFive(self):
        self.assertFalse(p.hasProperFormat("PRHSSX"))


if __name__ == '__main__':
    unittest.main()
