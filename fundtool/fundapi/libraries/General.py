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

        # response["price"] = self.get_price(fund_symbol)
        # response["min_investment"] = self.get_min_investment(fund_symbol)
        # response["expense_ratio"] = self.get_expense_ratio(fund_symbol)
        # response["asset_allocation"] = self.get_asset_allocation_data(fund_symbol)
        # response["morningstar_overall_rating"] = self.get_morningstar_overall_rating(fund_symbol)
        # response["morningstar_risk_vs_category"] = self.get_morningstar_risk_vs_category(fund_symbol)
        # response["morningstar_return_vs_category"] = self.get_morningstar_return_vs_category(fund_symbol)
        # response["morningstar_category"] = self.get_morningstar_category(fund_symbol)
        # response["turnover_ratio"] = self.get_turnover_ratio(fund_symbol)
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
        return {}

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
