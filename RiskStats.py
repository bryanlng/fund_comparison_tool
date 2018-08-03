from bs4 import BeautifulSoup
import requests
import json

class RiskStats:
    def get_risk_stats(fund_symbol):
        """
        Grabs risk stats. Grabs 8 things, for 4 time period of (3 year, 5 year, 10 year, 15 year):
            1. Alpha
            2. Beta
            3. R-squared
            4. Standard deviation
            5. Sharpe ratio
            6. Sortino ratio
            7. Treynor ratio
            8. Capture ratios (5 time periods: 1 year, 3 year, 5 year, 10 year, 15 year)
        Return in a JsonResponse encoded object
        """
        print ("")


    def get_alphas(fund_symbol):
        """
        Gets alpha values for 3 year, 5 year, 10 year, 15 year
        """
        print ("")


    def get_betas(fund_symbol):
        """
        Gets beta values for 3 year, 5 year, 10 year, 15 year
        """
        print ("")


    def get_r_squareds(fund_symbol):
        """
        Gets R-squared values for 3 year, 5 year, 10 year, 15 year
        """
        print ("")


    def get_stddevs(fund_symbol):
        """
        Gets standard deviation values for 3 year, 5 year, 10 year, 15 year
        """
        print ("")


    def get_sharpe_ratios(fund_symbol):
        """
        Gets sharpe ratios for 3 year, 5 year, 10 year, 15 year
        """
        print ("")


    def get_sortino_ratios(fund_symbol):
        """
        Gets sortino ratios for 3 year, 5 year, 10 year, 15 year
        """
        print ("")


    def get_treynor_ratios(fund_symbol):
        """
        Gets treynor ratios for 3 year, 5 year, 10 year, 15 year
        """
        print ("")


    def get_capture_ratios(fund_symbol):
        """
        Gets upside and downside capture ratios for 1 year, 3 year, 5 year, 10 year, 15 year
        """
        print ("")
