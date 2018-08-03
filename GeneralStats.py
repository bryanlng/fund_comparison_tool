from bs4 import BeautifulSoup
import requests
import json

class GeneralStats:
    def get_general_stats(fund_symbol):
        """
        Grabs general stats of the mutual fund. Grabs things:
            1. Price (NAV)
            2. Min. initial investment
            3. Expense ratio
            4. Symbol
            5. Asset allocation pie chart data(Morningstar's pie chart: Cash, US stock, Non-US stock, bonds, etc)
            6. Morningstar overall rating
            7. Morningstar risk vs category
            8. Morningstar return vs category
            9. Morningstar category
            10.Turnover ratio
        Source = Morningstar, quotes page
        """
        print ("")

    def get_price(fund_symbol):
        """
        Gets most up-to-date NAV of the mutual fund
        """
        print ("")

    def get_min_investment(fund_symbol):
        """
        Gets minimum amount of $$ required to invest in the mutual fund
        """
        print ("")

    def get_expense_ratio(fund_symbol):
        """
        Gets expense ratio (in percentage, ex: .77%)
        """
        print ("")

    def get_symbol(fund_symbol):
        """
        Gets 5 letter symbol of mutual fund (ex: PRHSX)
        """
        print ("")

    def get_asset_allocation_data(fund_symbol):
        """
        Gets the asset allocation data necessary for the pie chart
        Mimics Morningstar's asset allocation pie chart on the quotes page
        """
        print ("")

    def get_morningstar_overall_rating(fund_symbol):
        """
        Gets the overall Morningstar rating
        """
        print ("")

    def get_morningstar_risk_vs_category(fund_symbol):
        """
        Gets the overall risk compared to its category, as judged by Morningstar
        Found on quotes page
        """
        print ("")

    def get_morningstar_return_vs_category(fund_symbol):
        """
        Gets the overall return compared to its category, as judged by Morningstar
        Found on quotes page
        """
        print ("")

    def get_morningstar_category(fund_symbol):
        """
        Gets the type of category/sector the fund is in
        """
        print ("")

    def get_turnover_ratio(fund_symbol):
        """
        Gets turnover ratio of the mutual fund
        """
        print ("")
