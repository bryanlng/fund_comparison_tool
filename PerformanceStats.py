from bs4 import BeautifulSoup
import requests
import json


class PerformanceStats:
    def get_performance_stats(self, fund_symbol):
        """
        Grabs performance stats. Grabs 3 things:
            1. Data for the Growth of $10,000
            2. Trailing returns for the time periods (1 month, 3 month, 6 month, YTD, 1 year, 3 year, 5 year, 10 year, 15 year)
            3. Historical annual total returns for each year (current year until earliest date)
        Return in a JsonResponse encoded object
        """
        print("")

    def get_10000_growth(self, fund_symbol):
        print("")

    def get_trailing_returns(self, fund_symbol):
        """
        Grabs trailing returns for the time periods (1 month, 3 month, 6 month, YTD, 1 year, 3 year, 5 year, 10 year, 15 year)
        Source = Morningstar
        Input:      Fund symbol, 5 letter acronym, string
        Returns:    Dict with return values, key = time period, value = return
        """
        url = self.build_performance_url(fund_symbol)
        raw = requests.get(url)
        if raw != None:
            soup = BeautifulSoup(raw.text, 'html.parser')

            # Build a dictionary, where key = time period, value = trailing return for that time period.
            timespans = ["1-Month", "3-Month", "6-Month", "YTD",
                         "1-Year", "3-Year", "5-Year", "10-Year", "15-Year"]
            dictionary = {}

            # Find corresponding column values of trailing returns. These will be the values of the dict
            table = soup.find("table")
            rows = table.findAll(lambda tag: tag.name == 'tr')
            for row in rows:
                row_header = row.find("th")
                if row_header.text == fund_symbol:
                    quarterly_returns = [col.text for col in row.findAll("td")]
                    dictionary = dict(zip(timespans, quarterly_returns))
            return dictionary

    def build_performance_url(self, fund_symbol):
        return "http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=" + fund_symbol + "&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype="

    def get_fund_historical_returns(self, fund_symbol):
        """
        Grabs historical annual total returns for each year (current year until earliest date),
        for both the fund, and its category
        Source = Yahoo Finance
        Input:      Fund symbol, 5 letter acronym, string
        Returns:    Dict that contains 2 dicts. Each dict has key=year, value=return
        """
        url = self.build_historical_url(fund_symbol)
        raw = requests.get(url)
        if raw != None:
            soup = BeautifulSoup(raw.text, 'html.parser')

    def build_historical_url(self, fund_symbol):
        return


p = PerformanceStats()
print(p.get_trailing_returns("PRHSX"))
