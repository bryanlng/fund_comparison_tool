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


        Groups in terms of GET requests:
        1. header request:
            response["price"] = self.get_price(fund_symbol)
            response["min_investment"] = self.get_min_investment(fund_symbol)
            response["expense_ratio"] = self.get_expense_ratio(fund_symbol)
            response["turnover_ratio"] = self.get_turnover_ratio(fund_symbol)
            response["morningstar_category"] = self.get_morningstar_category(fund_symbol)

        2. asset allocation
            response["asset_allocation"] = self.get_asset_allocation_data(fund_symbol)

        3. risk measures
            response["morningstar_risk_vs_category"] = self.get_morningstar_risk_vs_category(fund_symbol)
            response["morningstar_return_vs_category"] = self.get_morningstar_return_vs_category(fund_symbol)

        4. security identifier get request
            response["morningstar_overall_rating"] = self.get_morningstar_overall_rating(fund_symbol)
        """

        response = {}


        response["price"] = self.get_price(fund_symbol)
        response["min_investment"] = self.get_min_investment(fund_symbol)
        response["expense_ratio"] = self.get_expense_ratio(fund_symbol)
        response["asset_allocation"] = self.get_asset_allocation_data(fund_symbol)
        response["morningstar_overall_rating"] = self.get_morningstar_overall_rating(fund_symbol)
        response["morningstar_risk_vs_category"] = self.get_morningstar_risk_vs_category(fund_symbol)
        response["morningstar_return_vs_category"] = self.get_morningstar_return_vs_category(fund_symbol)
        response["morningstar_category"] = self.get_morningstar_category(fund_symbol)
        response["turnover_ratio"] = self.get_turnover_ratio(fund_symbol)
        return {}


    def get_price(self, fund_symbol):
        """
        Gets most up-to-date NAV of the mutual fund
        """
        return {}

    def get_min_investment(self, fund_symbol):
        """
        Gets minimum amount of $$ required to invest in the mutual fund
        """
        return {}

    def get_expense_ratio(self, fund_symbol):
        """
        Gets expense ratio (in percentage, ex: .77%)
        """
        return {}

    def get_asset_allocation_data(self, fund_symbol):
        """
        Gets the asset allocation data necessary for the pie chart
        Mimics Morningstar's asset allocation pie chart on the quotes page
        """
        return {}

    def get_morningstar_overall_rating(self, fund_symbol):
        """
        Gets the overall Morningstar rating
        """
        return {}

    def get_morningstar_risk_vs_category(self, fund_symbol):
        """
        Gets the overall risk compared to its category, as judged by Morningstar
        Found on quotes page
        """
        return {}

    def get_morningstar_return_vs_category(self, fund_symbol):
        """
        Gets the overall return compared to its category, as judged by Morningstar
        Found on quotes page
        """
        return {}

    def get_morningstar_category(self, fund_symbol):
        """
        Gets the type of category/sector the fund is in
        """
        return {}

    def get_turnover_ratio(self, fund_symbol):
        """
        Gets turnover ratio of the mutual fund
        """
        return {}
