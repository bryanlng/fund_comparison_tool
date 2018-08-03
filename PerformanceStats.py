from bs4 import BeautifulSoup
import requests
import json

class PerformanceStats:
    def get_performance_stats(fund_symbol):
        """
        Grabs performance stats. Grabs 3 things:
            1. Data for the Growth of $10,000
            2. Trailing returns for the time periods (1 month, 3 month, 6 month, YTD, 1 year, 3 year, 5 year, 10 year, 15 year)
            3. Historical annual total returns for each year (current year until earliest date)
        Return in a JsonResponse encoded object
        """
        print ""


    def get_trailing_returns(fund_symbol):
        """
        Grabs trailing returns for the time periods (1 month, 3 month, 6 month, YTD, 1 year, 3 year, 5 year, 10 year, 15 year)
        Source = Morningstar
        """
        print ""


    def get_historical_returns(fund_symbol):
        """
        Grabs historical annual total returns for each year (current year until earliest date)
        Source = Yahoo Finance
        """
        print ""
