import unittest

import PerformanceStats

class UtilTests(unittest.TestCase):

    p = PerformanceStats()

    def testHappyPath(self):
        self.assertTrue(p.hasGoodSyntax("PRHSX"))

    def testContainsNumbers(self):
        self.assertFalse(p.hasGoodSyntax("334SX"))

    def testEmpty(self):
        self.assertFalse(p.hasGoodSyntax(""))

    def testNotLengthofFive(self):
        self.assertFalse(p.hasGoodSyntax("PRHX"))

    def testLowerCase(self):
        self.assertFalse(p.hasGoodSyntax("PRsHX"))

    def testGreaterLengthofFive(self):
        self.assertFalse(p.hasGoodSyntax("PRHSSX"))


if __name__ == '__main__':
    unittest.main()
