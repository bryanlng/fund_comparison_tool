from bs4 import BeautifulSoup
from lxml import etree, html
import requests
import json

import fundapi.libraries.util as Util
from fundapi.libraries.util import Section
import fundapi.libraries.exceptions as FundException

class HoldingsStats:
    def get_holdings_stats(self, fund_symbol):
        """
        Gets the top 25 companies in their portfolio, as well as the following stats:
            1. Name
            2. % portfolio weight
            3. YTD return

        First get the first 25 most weighted companies from portfolio (desc), then bottom 25 (asc)
        For each:
            1. Equity view tab
                -Name
                -% portfolio weight
                -Shares owned
                -Shares changed
                -YTD return
                -P/E
            2. Equity prices tab
                -Price
                -G/L % (gain/loss percent)

        Comparisons between 2+ mutual funds will compare Name and % portfolio weight only
        """
        response = {"holdings": "test"}
        section = Section.HOLDINGS_PAGE_BOTTOM_25
        url = Util.build_url(section, fund_symbol)

        raw = requests.get(url)
        raw_data = raw.json()
        data = raw_data["htmlStr"]
        # print(data)

        data = data.strip()
        data = data.replace("\n", "")
        data = data.replace("\t", "")
        print(data)

        response["data"] = data

        return response
