from bs4 import BeautifulSoup
import requests
import json

class HoldingsStats:
    def get_holdings(fund_symbol):
        """
        Gets the top 25 companies in their portfolio, as well as the following stats:
            1. Name
            2. % portfolio weight
            3. YTD return
        """
        print ""
