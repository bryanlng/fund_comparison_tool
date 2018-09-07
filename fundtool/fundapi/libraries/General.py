from bs4 import BeautifulSoup
import requests
import json
from lxml import etree, html

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

        fund_symbol = fund_symbol.upper()
        response = {}

        try:
            Util.validate_format(fund_symbol)
            sections = [Section.GENERAL_STATS, Section.ASSET_ALLOCATION, Section.RISK_RETURN_VS_CATEGORY, Section.OVERALL_RATING]
            for section in sections:
                response[str(section)] = self.get_section_data(section, fund_symbol)

        except FundException.ImproperSymbolFormatError as e:
            raise FundException.ImproperSymbolFormatError(e)
        except FundException.SymbolDoesNotExistError as e:
            raise FundException.SymbolDoesNotExistError(e)
        except FundException.UIChangedError as e:
            raise FundException.UIChangedError(e)
        except FundException.SourceEndpointChangedError as e:
            raise FundException.SourceEndpointChangedError(e)

        return response


    def get_section_data(self, section, fund_symbol):
        response = {}

        url = ""
        if section == Section.OVERALL_RATING:
            performanceId = self.extract_performance_id(fund_symbol)
            url = Util.build_url(section, fund_symbol, 0, performanceId)
        else:
            url = Util.build_url(section, fund_symbol)

        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            print("200 and not empty")
            soup = BeautifulSoup(raw.text, 'html.parser')
            return self.extract_column_data(section, soup, raw)

        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for trailing returns: Symbol does not exist: {fund_symbol}")

    def extract_column_data(self, section, soup, raw):
        response = {}

        if section == Section.OVERALL_RATING:
            data = raw.json()
            if "starRating" in data:
                response["starRating"] = data["starRating"]
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for trailing returns: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")

        elif section == Section.GENERAL_STATS:
            keys = ["NAV", "MinInvestment", "ExpenseRatio", "Turnover", "MorningstarCategory"]
            for key in keys:
                spans = soup.findAll("span", attrs={"vkey": key})
                if len(spans) > 0:
                    span = spans[0]
                    span_text = span.text
                    response[key] = span_text.strip()

        elif section == Section.ASSET_ALLOCATION:
            fields = ["Cash", "US Stock", "US Stocks", "Non US Stock", "Non US Stocks", "Bond", "Bonds", "Other"]
            table = soup.find("table")
            if table is not None:
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    rowData = [col.text for col in row.findAll("td") if col.text != ""]
                    if len(rowData) > 0:
                        fieldEntry = rowData[0]
                        if fieldEntry in fields:
                            response[fieldEntry] = rowData[1]
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for trailing returns: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")

        else:
            fields = ["Risk vs.Category", "Return vs.Category"]
            table = soup.find("table")
            if table is not None:
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    rowData = [col.text.strip() for col in row.findAll("td") if col.text.strip() != ""]
                    if len(rowData) > 0:
                        fieldEntry = rowData[0]
                        for field in fields:
                            if fieldEntry.find(field) != -1:
                                response[field] = rowData[1]
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for trailing returns: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")

        return response


    def extract_performance_id(self, fund_symbol):
        """
        Extract id from page, so get_morningstar_overall_rating() can build a url that can get the actual star rating
        """
        url = Util.build_url(Section.QUOTES_PAGE, fund_symbol)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            #Build lxml tree from webpage
            tree = html.fromstring(raw.content)

            #Find the meta tag that says "performanceId", and extract the content field
            tags = tree.xpath('.//meta[@name="performanceId"]')
            tag = tags[0]
            return tag.get("content")
