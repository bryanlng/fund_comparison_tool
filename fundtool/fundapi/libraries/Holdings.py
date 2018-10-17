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
            4. Shares owned
            5. Shares changed
            6. P/E
            7. Price
            8. G/L % (gain/loss percent for the day)

        First get the first 25 most weighted companies from portfolio (desc)
        For each:
            1. Equity view tab
                -Name
                -% portfolio weight
                -Shares owned
                -Shares changed
                -YTD return (could be positive, negative, float, or blank (-) )
                -P/E (could be positive, negative, float, or blank (-) )
            2. Equity prices tab
                -Price
                -G/L % (gain/loss percent)

        Each tab is represented as a table
            -equity view tab:       id = equity_holding_tab
                -get <tbody> with id holding_epage0
            -equity prices tab:     id = equityPrice_holding_tab

        Comparisons between 2+ mutual funds will compare Name and % portfolio weight only
        """

        fund_symbol = fund_symbol.upper()
        response = {}

        try:
            Util.validate_format(fund_symbol)
            url = Util.build_url(Section.HOLDINGS_PAGE_TOP_25, fund_symbol)
            response = self.extractHoldings(url, fund_symbol)

        except FundException.ImproperSymbolFormatError as e:
            raise FundException.ImproperSymbolFormatError(e)
        except FundException.SymbolDoesNotExistError as e:
            raise FundException.SymbolDoesNotExistError(e)
        except FundException.UIChangedError as e:
            raise FundException.UIChangedError(e)
        except FundException.SourceEndpointChangedError as e:
            raise FundException.SourceEndpointChangedError(e)

        return response

    def extractHoldings(self, url, fund_symbol):
        response = {}
        raw_data = self.pullData(url, fund_symbol)
        if raw_data != None:
            return self.parseData(raw_data, fund_symbol)

    def pullData(self, url, fund_symbol):
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            raw_data = raw.json()
            data = raw_data["htmlStr"]
            return self.filterSpecialChars(data)
        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for holdings data: Symbol does not exist: {fund_symbol}")

    def parseData(self, data, fund_symbol):
        response = {}
        soup = BeautifulSoup(data, 'html.parser')
        tabs = ["equity_holding_tab", "equityPrice_holding_tab"]
        for tab in tabs:
            table = soup.find("table", id=tab)
            if table is not None:
                tbody = table.find('tbody')
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    #Extract stock name
                    row_header = row.find("th")
                    if row_header is not None:
                        stock_name = row_header.text

                        #Extract details for that stock
                        stats = [col.text.strip() for col in row.findAll("td") if col.text.strip() != ""]
                        if len(stats) > 1:
                            statsDict = self.buildStatsDict(tab, stats)

                            if stock_name not in response:
                                response[stock_name] = statsDict
                            else:
                                current_dict = response[stock_name]
                                current_dict = {**current_dict, **statsDict}
                                response[stock_name] = current_dict
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for holdings data: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
        return response

    def filterSpecialChars(self, data):
        data = data.strip()
        data = data.replace("\n", "")
        data = data.replace("\t", "")
        return data

    def buildStatsDict(self, tabId, stats):
        fields = []
        if tabId == "equity_holding_tab":
            del stats[2:5]
            fields = ["% portfolio weight", "Shares Owned", "Country", "YTD Return", "P/E ratio"]
        else:
            stats = stats[2:5]
            fields = ["Currency", "Price", "Gain/Loss %"]

        return dict(zip(fields, stats))
