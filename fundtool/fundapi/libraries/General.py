from bs4 import BeautifulSoup
import requests
import json

import fundapi.libraries.util as Util
from fundapi.libraries.util import Section
import fundapi.libraries.exceptions as FundException

class GeneralStats:
    def get_general_stats(self, fund_symbol):
        """
        Grabs general stats of the mutual fund. Grabs things:
            1. Price (NAV)
            2. Min. initial investment
            3. Expense ratio
            4. Asset allocation pie chart data(Morningstar's pie chart: Cash, US stock, Non-US stock, bonds, etc)Asset allocation pie chart data(Morningstar's pie chart: Cash, US stock, Non-US stock, bonds, etc)
            5. Morningstar overall rating
            6. Morningstar risk vs category
            7. Morningstar return vs category
            8. Morningstar category
            9. Turnover ratio
        Source = Morningstar, quotes page
        """

        response = {}

        sections = [Section.GENERAL_STATS, Section.ASSET_ALLOCATION, Section.RISK_RETURN_VS_CATEGORY, Section.OVERALL_RATING]
        # for section in sections:

        response["price"] = self.get_general_details(fund_symbol)
        # response["min_investment"] = self.get_asset_allocation_data(fund_symbol)
        # response["expense_ratio"] = self.get_risk_return_vs_category(fund_symbol)
        # response["asset_allocation"] = self.get_asset_allocation_data(fund_symbol)
        return {}


    def get_general_details(self, fund_symbol):
        """
        Gets the following:
            1. Price/ NAV
            2. Minimum investment
            3. Expense ratio (in percentage, ex: .77%)
            4. Turnover ratio (in percentage, ex: .77%)
            5. Morningstar Category
        """
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        timespans = ["1-Month", "3-Month", "6-Month", "YTD",
                     "1-Year", "3-Year", "5-Year", "10-Year", "15-Year"]
        response = {}
        url = Util.build_url(Section.GENERAL_STATS, fund_symbol)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            print("200 and not empty")
            soup = BeautifulSoup(raw.text, 'html.parser')

            # Find Values
            """
            NAV:
                <span vkey="NAV">
                 82.70
                </span>

            Minimum investment:
            <span ckey="isCur" vkey="MinInvestment">
                2,500
            </span>

            Expense ratio:
                <span vkey="ExpenseRatio" class="gr_text1">
                     0.77%
                </span>

            Turnover ratio:
            <span vkey="Turnover" class="gr_text1">
                 38%
            </span>

            Morningstar category:
            <span vkey="MorningstarCategory" class="gr_text1">
                 Health
            </span>
            """
            divs = soup.find_all("span", attrs={"vkey": "NAV"})
            print(divs)

        #     else:
        #         raise FundException.UIChangedError(f"Error while retrieving data for trailing returns: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
        # else:
        #     raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for trailing returns: Symbol does not exist: {fund_symbol}")

        return response

    def get_asset_allocation_data(self, fund_symbol):
        """
        Gets the asset allocation data necessary for the pie chart
        Mimics Morningstar's asset allocation pie chart on the quotes page
        """
        return {}

    def get_risk_return_vs_category(self, fund_symbol):
        """
        Gets the:
            1. overall risk compared to its category, as judged by Morningstar
            2. overall return compared to its category, as judged by Morningstar
        Found on quotes page
        """
        return {}

    def get_morningstar_overall_rating(self, fund_symbol):
        """
        Gets the overall Morningstar rating
        """
        return {}
