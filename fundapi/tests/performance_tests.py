from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from unittest.mock import patch

# Create your tests here.

from fundapi.libraries.Performance import PerformanceStats
import fundapi.libraries.exceptions as FundException

class PerformanceEndpointTest(TestCase):
    """
    This class defines the test suite for the PerformanceEndpointTest view.
    """

    PERFORMANCE_ENDPOINT = '/v1/performance/'
    PerformanceStatsHelper = PerformanceStats()


    def setUp(self):
        self.client = APIClient()

    @patch.object(PerformanceStatsHelper, 'get_10000_growth')
    @patch.object(PerformanceStatsHelper, 'get_fund_historical_returns')
    def test_trailing_returns_good_symbol_name(self,
                                               mock_get_fund_historical_returns,
                                               mock_get_10000_growth):
        fund_symbol = "PRHSX"

        #Scrape actual data using selenium
        expected_trailing_returns = {

        }
        expected_historical_returns = {
            "PRHSX": {
              "1996": 26.75,
              "1997": 19.41,
              "1998": 22.37,
              "1999": 7.97,
              "2000": 52.19,
              "2001": -5.97,
              "2002": -27.74,
              "2003": 37.49,
              "2004": 15.84,
              "2005": 13.53,
              "2006": 9.58,
              "2007": 18.75,
              "2008": -28.77,
              "2009": 32.17,
              "2010": 16.33,
              "2011": 11.01,
              "2012": 31.93,
              "2013": 51.4,
              "2014": 31.94,
              "2015": 12.98,
              "2016": -10.35,
              "2017": 27.95
            },
            "Category": {
              "1996": 13.5,
              "1997": 22.11,
              "1998": 20.97,
              "1999": 18.58,
              "2000": 56.75,
              "2001": -11.26,
              "2002": -28.13,
              "2003": 32.51,
              "2004": 9.84,
              "2005": 9.64,
              "2006": 4.27,
              "2007": 9.27,
              "2008": -23.43,
              "2009": 22.48,
              "2010": 8.38,
              "2011": 7.66,
              "2012": 21.55,
              "2013": 48.17,
              "2014": 27.25,
              "2015": 8.05,
              "2016": -10.6,
              "2017": 24.31
            }
        }
        expected_10000_growth = {

        }


        expected = {
            "trailing_returns": expected_trailing_returns,
            "historical_returns": expected_historical_returns,
            "10000_growth_data": expected_10000_growth
        }

        mock_get_fund_historical_returns.return_value = expected_historical_returns
        mock_get_10000_growth.return_value = expected_10000_growth

        actual = self.client.get(
            self.PERFORMANCE_ENDPOINT + fund_symbol,
            {'pretty': True}
        )

        self.assertEqual(200, actual.status_code)
        self.assertEqual(expected, actual.json())


    def test_trailing_returns_symbol_improper_syntax(self):
        fund_symbol = "1rrfr"
        error_message = "Fund symbol is not in the proper format (needs to be 5 characters, capitalized, no spaces, A-Z): " + fund_symbol
        expected = {
            'error': = error_message,
            'HTTP_ERROR_CODE' = 400
        }

        actual = self.client.get(
            self.PERFORMANCE_ENDPOINT + fund_symbol,
            {'pretty': True}
        )

        self.assertEqual(400, actual.status_code)
        self.assertEqual(expected, actual.json())


    def test_trailing_returns_symbol_not_exist(self):
        fund_symbol = "GGGGG"
        error_message = "Error while retrieving data for trailing returns: Symbol does not exist: " + fund_symbol
        expected = {
            'error': = error_message,
            'HTTP_ERROR_CODE' = 404
        }

        actual = self.client.get(
            self.PERFORMANCE_ENDPOINT + fund_symbol,
            {'pretty': True}
        )

        self.assertEqual(404, actual.status_code)
        self.assertEqual(expected, actual.json())
