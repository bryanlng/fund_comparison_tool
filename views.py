from bs4 import BeautifulSoup
import requests
import json

"""
https://stackoverflow.com/questions/17196018/extracting-table-contents-from-html-with-python-and-beautifulsoup
http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=XNAS:PRHSX&region=usa&culture=en-US&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype=

difference between daily, monthly, quarterly, is in align field. For quarterly, align="q"
https://stackoverflow.com/questions/209840/convert-two-lists-into-a-dictionary-in-python
"""

url = "http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=XNAS:PRHSX&region=usa&culture=en-US&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype="
raw = requests.get(url)
text = raw.text
soup = BeautifulSoup(text, 'html.parser')
table = soup.find("table")
rows = table.findAll(lambda tag: tag.name == 'tr')
dictionary = {}  # Dictionary: key = time period, value = trailing return for that time period. Ex: {u'3-Month': u'6.31', u'1-Month': u'1.57', u'3-Year': u'5.11', u'10-Year': u'17.19', u'15-Year': u'15.35', u'6-Month': u'7.75', u'YTD': u'7.75', u'1-Year': u'15.32', u'5-Year': u'18.52'}

# Find time span values of trailing returns. These will be the keys of the dict
th_timespans = rows[0].findAll("th")
timespans = [
    timespan.text for timespan in th_timespans if "Total Return " not in timespan.text]
# print(timespans)

# Find corresponding column values of trailing returns. These will be the values of the dict
for row in rows:
    # print row
    row_header = row.find("th")
    if row_header.text == "PRHSX":
        # print row_header.text
        cols = row.findAll("td")
        column_values = [col.text for col in cols]

        # Create dictionary from timespans and column_values
        dictionary = dict(zip(timespans, column_values))
        print(dictionary)
    # print row
    # print ""
# print(type(rows))
# print(rows)


################################################################################################################################
# General stats
################################################################################################################################
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
    print ""

def get_price(fund_symbol):
    """
    Gets most up-to-date NAV of the mutual fund
    """
    print ""

def get_min_investment(fund_symbol):
    """
    Gets minimum amount of $$ required to invest in the mutual fund
    """
    print ""

def get_expense_ratio(fund_symbol):
    """
    Gets expense ratio (in percentage, ex: .77%)
    """
    print ""

def get_symbol(fund_symbol):
    """
    Gets 5 letter symbol of mutual fund (ex: PRHSX)
    """
    print ""

def get_asset_allocation_data(fund_symbol):
    """
    Gets the asset allocation data necessary for the pie chart
    Mimics Morningstar's asset allocation pie chart on the quotes page
    """
    print ""

def get_morningstar_overall_rating(fund_symbol):
    """
    Gets the overall Morningstar rating
    """
    print ""

def get_morningstar_risk_vs_category(fund_symbol):
    """
    Gets the overall risk compared to its category, as judged by Morningstar
    Found on quotes page
    """
    print ""

def get_morningstar_return_vs_category(fund_symbol):
    """
    Gets the overall return compared to its category, as judged by Morningstar
    Found on quotes page
    """
    print ""

def get_morningstar_category(fund_symbol):
    """
    Gets the type of category/sector the fund is in
    """
    print ""

def get_turnover_ratio(fund_symbol):
    """
    Gets turnover ratio of the mutual fund
    """
    print ""

################################################################################################################################
# Performance stats
################################################################################################################################

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


################################################################################################################################
# Risk stats
################################################################################################################################

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
    print ""


def get_alphas(fund_symbol):
    """
    Gets alpha values for 3 year, 5 year, 10 year, 15 year
    """
    print ""


def get_betas(fund_symbol):
    """
    Gets beta values for 3 year, 5 year, 10 year, 15 year
    """
    print ""


def get_r_squareds(fund_symbol):
    """
    Gets R-squared values for 3 year, 5 year, 10 year, 15 year
    """
    print ""


def get_stddevs(fund_symbol):
    """
    Gets standard deviation values for 3 year, 5 year, 10 year, 15 year
    """
    print ""


def get_sharpe_ratios(fund_symbol):
    """
    Gets sharpe ratios for 3 year, 5 year, 10 year, 15 year
    """
    print ""


def get_sortino_ratios(fund_symbol):
    """
    Gets sortino ratios for 3 year, 5 year, 10 year, 15 year
    """
    print ""


def get_treynor_ratios(fund_symbol):
    """
    Gets treynor ratios for 3 year, 5 year, 10 year, 15 year
    """
    print ""


def get_capture_ratios(fund_symbol):
    """
    Gets upside and downside capture ratios for 1 year, 3 year, 5 year, 10 year, 15 year
    """
    print ""


################################################################################################################################
#Holdings (companies)
################################################################################################################################

def get_holdings(fund_symbol):
    """
    Gets the top 25 companies in their portfolio, as well as the following stats:
        1. Name
        2. % portfolio weight
        3. YTD return
    """
    print ""
