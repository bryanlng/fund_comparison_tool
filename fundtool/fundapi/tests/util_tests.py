import unittest
from fundapi.libraries.Performance import PerformanceStats
import fundapi.libraries.util
from fundapi.libraries.util import Section

class ValidateFormatTests(unittest.TestCase):
    def testHappyPath(self):
        self.assertTrue(Util.validate_format("PRHSX"))

    def testHappyPathButNotAnActualSymbo(self):
        self.assertTrue(Util.validate_format("ZZZZZ"))

    def testContainsNumbers(self):
        self.assertFalse(Util.validate_format("334SX"))

    def testContainsSlash(self):
        self.assertFalse(Util.validate_format("33/SX"))

    def testEmpty(self):
        self.assertFalse(Util.validate_format(""))

    def testNotLengthofFive(self):
        self.assertFalse(Util.validate_format("PRHX"))

    def testLowerCase(self):
        self.assertFalse(Util.validate_format("PRsHX"))

    def testGreaterLengthofFive(self):
        self.assertFalse(Util.validate_format("PRHSSX"))

class BuildUrlTests(unittest.TestCase):
    def testTrailing(self):
        fund_symbol = "PRHSX"
        expected = "http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=" + fund_symbol + "&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype="
        self.assertEqual(Util.build_url(Section.TRAILING, fund_symbol), expected)

    def testGrowth(self):
        fund_symbol = "PRHSX"
        expected = "https://markets.ft.com/data/funds/ajax/US/get-comparison-panel?data={\"comparisons\":[\"" + fund_symbol + "\"],\"openPanels\":[\"Performance\"]}"
        self.assertEqual(Util.build_url(Section.GROWTH, fund_symbol), expected)

    def testHistorical(self):
        fund_symbol = "PRHSX"
        expected = "https://finance.yahoo.com/quote/" + fund_symbol + "/performance?p=" + fund_symbol
        self.assertEqual(Util.build_url(Section.HISTORICAL, fund_symbol), expected)


if __name__ == '__main__':
    unittest.main()
