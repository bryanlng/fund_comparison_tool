from bs4 import BeautifulSoup
import requests
import json

import fundapi.libraries.util as Util
from fundapi.libraries.util import Section
import fundapi.libraries.exceptions as FundException

class RiskStats:
    def get_risk_stats(self, fund_symbol):
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

        #Add data from capture ratios first. We can get all data in capture ratios in 1 get request, but need multiple for mpt and volatility
        fund_symbol = fund_symbol.upper()
        response = {}
        try:
            Util.validate_format(fund_symbol)
            response = self.get_capture_ratios(fund_symbol)
            timespans = ["3-Year", "5-Year", "10-Year", "15-Year"]
            for timespan in timespans:
                #Extract and aggregate data for MPT stats and Volatility stats
                mpt_and_volatility = self.collect_column_data(fund_symbol, timespan)

                #Add these values into the current timespan dict along with the capture ratios
                response[timespan] = {**response[timespan], **mpt_and_volatility}

        except FundException.ImproperSymbolFormatError as e:
            raise FundException.ImproperSymbolFormatError(e)
        except FundException.SymbolDoesNotExistError as e:
            raise FundException.SymbolDoesNotExistError(e)
        except FundException.UIChangedError as e:
            raise FundException.UIChangedError(e)
        except FundException.SourceEndpointChangedError as e:
            raise FundException.SourceEndpointChangedError(e)

        return response


    def collect_column_data(self,fund_symbol, timespan):
        """
        For a given timespan, gets ALL the MPT + Volatility data
        """
        timespan_dict = {}
        year = timespan.split("-")[0]
        sections = [Section.RISK_MPT, Section.RISK_VOLATILITY]

        for section in sections:
            section_dict = {}
            url = Util.build_url(section, fund_symbol, year)
            raw = requests.get(url)
            if raw.status_code == 200 and raw.text != "":
                print("200 and not empty")
                soup = BeautifulSoup(raw.text, 'html.parser')

                # Find corresponding column values of trailing risk stats. These will be the values of the dict
                dataNotFoundYet = True
                table = soup.find("table")
                if table is not None:
                    rows = table.findAll(lambda tag: tag.name == 'tr')
                    for row in rows:
                        row_header = row.find("th")
                        if dataNotFoundYet and row_header != None and row_header.text == fund_symbol:
                            dataNotFoundYet = False
                            section_dict = self.extract_column_data(row, section)

                            #Accumulate key-value pairs of section_dict into timespan_dict
                            timespan_dict = {**timespan_dict, **section_dict}
                else:
                    raise FundException.UIChangedError(f"Error while retrieving data for risk mpt: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
            else:
                raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for risk mpt: Symbol does not exist: {fund_symbol}")

        return timespan_dict

    def extract_column_data(self, row, section):
        response = {}
        if section == Section.RISK_MPT:
            fields = ["Category Index", "R-Squared", "Beta", "Alpha", "Treynor Ratio", "Currency"]
            stats = [col.text.strip() for col in row.findAll("td")]
            response = dict(zip(fields, stats))
        else:
            fields = ["Standard Deviation", "Return", "Sharpe Ratio", "Sortino Ratio"]
            stats = [col.text.strip() for col in row.findAll("td")]
            del stats[len(stats)-1]                             #Remove unnecessary values
            response = dict(zip(fields, stats))
        return response

    def get_capture_ratios(self, fund_symbol):
        """
        Gets upside and downside capture ratios for 1 year, 3 year, 5 year, 10 year, 15 year
        """
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        timespans = ["3-Year", "5-Year", "10-Year", "15-Year"]
        fields = ["Standard Deviation", "Return", "Sharpe Ratio", "Sortino Ratio"]
        response = {}

        url = Util.build_url(Section.CAPTURE_RATIOS, fund_symbol)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            print("200 and not empty")
            soup = BeautifulSoup(raw.text, 'html.parser')

            # Find corresponding column values of trailing risk stats. These will be the values of the dict
            table = soup.find("table")
            if table is not None:
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    row_header = row.find("th")
                    if row_header != None and row_header.text == fund_symbol:
                        stats = []
                        for col in row.findAll("td"):
                            #Values are stuck together. Ex: Convert "145.9576.71" --> "145.95", "76.71"
                            raw = col.text
                            first_dot = raw.find(".")
                            upside_ratio = raw[:first_dot+3]
                            downside_ratio = raw[first_dot+3:]
                            stats.append({"Upside Ratio": upside_ratio, "Downside ratio": downside_ratio})

                        del stats[0]       #Delete 1-Year for consistency, since other stats only have 3year, 5year, 10year, 15year
                        response = dict(zip(timespans, stats))
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for risk capture ratios: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for risk capture ratios: Symbol does not exist: {fund_symbol}")

        return response
