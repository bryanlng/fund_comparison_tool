from bs4 import BeautifulSoup
import requests
import json
import datetime
from lxml import etree, html
import ast

class PerformanceStats:

    def get_performance_stats(self, fund_symbol):
        """
        Grabs performance stats. Grabs 3 things:
            1. Data for the Growth of $10,000
            2. Trailing returns for the time periods (1 month, 3 month, 6 month, YTD, 1 year, 3 year, 5 year, 10 year, 15 year)
            3. Historical annual total returns for each year (current year until earliest date)
        Return in a JsonResponse encoded object
        """
        stats = {}
        stats["trailing_returns"] = self.get_trailing_returns(fund_symbol)
        stats["historical_returns"] = self.get_fund_historical_returns(fund_symbol)
        stats["10000_growth_data"] = self.get_10000_growth(fund_symbol)
        return stats

    def build_10000_growth_url(self, fund_symbol):
        return "https://markets.ft.com/data/funds/ajax/US/get-comparison-panel?data={\"comparisons\":[\"" + fund_symbol + "\"],\"openPanels\":[\"Performance\"]}"

    def get_10000_growth(self, fund_symbol):
        """
        Grabs data for hypothetical growth of $10000 
        Source = markets.ft
        https://stackoverflow.com/questions/11205386/python-beautifulsoup-get-an-attribute-value-based-on-the-name-attribute
        https://codereview.stackexchange.com/questions/106719/converting-string-to-dict-using-python-ast-library
        
        Returns:
            -A dictionary where key = date (YYYY-MM-DD, removing the "T00:00:00" from the end), value = expected dollar value that year
        """
        response = {}
        url = self.build_10000_growth_url(fund_symbol)
        raw_data = requests.get(url)
        if raw_data.status_code == 200:
            raw_json = raw_data.json();
            html = raw_json["html"]

            #Interpret HTML using BeautifulSoup, then extract out data in JSON from <div data_mod_config = ...., class = mod-ui-chart--dynamic>
            soup = BeautifulSoup(html, 'html.parser')
            data_mod_config_div = soup.find("div", {"class": "mod-ui-chart--dynamic"})["data-mod-config"]
            growth_json = ast.literal_eval(data_mod_config_div)
            internal_data = growth_json["data"]
            if len(internal_data) >= 1:

                #Access first element in the dict, which is the list of values
                growths = next(iter(internal_data.values()))

                #Parse into a dict where key = date (YYYY-MM-DD, removing the "T00:00:00" from the end), value = expected dollar value that year
                return {year["date"][:len(year["date"])-9] : year["value"] for year in growths}



    def get_trailing_returns(self, fund_symbol):
        """
        Grabs trailing returns for the time periods (1 month, 3 month, 6 month, YTD, 1 year, 3 year, 5 year, 10 year, 15 year)
        Source = Morningstar
        Input:      Fund symbol, 5 letter acronym, string
        Returns:    Dict with return values, key = time period, value = return
        """
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        timespans = ["1-Month", "3-Month", "6-Month", "YTD",
                     "1-Year", "3-Year", "5-Year", "10-Year", "15-Year"]
        response = {}
        url = self.build_performance_url(fund_symbol)
        try:
            raw = requests.get(url)
            if raw.status_code == 200:
                soup = BeautifulSoup(raw.text, 'html.parser')

                # Find corresponding column values of trailing returns. These will be the values of the dict
                table = soup.find("table")
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    row_header = row.find("th")
                    if row_header.text == fund_symbol:
                        quarterly_returns = [col.text for col in row.findAll("td")]
                        response = dict(zip(timespans, quarterly_returns))
        except Exception as e: # Not good to have a catch-all exception, but I'll create custom exceptions later
            print(e)

        return response


    def build_performance_url(self, fund_symbol):
        return "http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=" + fund_symbol + "&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype="

    def get_fund_historical_returns(self, fund_symbol):
        """
        Grabs historical annual total returns for each year (current year until earliest date), for both the fund, and its category
        Source = Yahoo Finance
        Input:      Fund symbol, 5 letter acronym, string
        Returns:    Dict that contains 2 dicts (one for the fund, one for the category). Each dict has key=year, value=return
        """
        url = self.build_historical_url(fund_symbol)
        raw = requests.get(url)
        if raw != None:
            historical_returns = self.scrape_historical_returns(fund_symbol, url)
            if historical_returns != None:
                return historical_returns

    def build_historical_url(self, fund_symbol):
        return "https://finance.yahoo.com/quote/" + fund_symbol + "/performance?p=" + fund_symbol

    def scrape_historical_returns(self, fund_symbol, url):
        columns = self.extract_raw_column_data(fund_symbol, url)
        return self.build_json_response(columns, fund_symbol)

    def extract_raw_column_data(self, fund_symbol, url):
        """
        Extracts column data as Element objects from url

        https://stackoverflow.com/questions/14299978/how-to-use-lxml-to-find-an-element-by-text

        Process:
            Given this html from https://finance.yahoo.com/quote/PRHSX/performance?p=PRHSX:
            <div class="Mb(25px) " data-reactid="121">
                 <h3 data-reactid="122">
                    <span data-reactid="123">Annual Total Return (%) History</span>     <--Start here
                </h3>
                 <div data-reactid="124">
                    <div class="Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(20px) Pt(10px) C($c-fuji-grey-j) Fz(xs) Fw(400)" data-reactid="125">some irrelevant stuff here</div>  <-- remove
                    <div class="Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)" data-reactid="134"> Data column for 2018 with 4 spans, ignore </div>  <-- remove
                    <div class="Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)" data-reactid="134"> Data column for 2017 with 4 spans that we want to extract </div>
                    ....
                    <div class="Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)" data-reactid="134"> Data column for 1996 with 4 spans that we want to extract </div>

            1. Find the span tag that has text "Annual Total Return (%) History". This our starting point
            2. Navigate up to its parent tag, then go to sibiling tag that has the data we actually need, then grab that data
        """

        #Build lxml tree from webpage
        page = requests.get(url)
        tree = html.fromstring(page.content)

        #Find the H3 tag that says Annual Total Return (%) History
        h3_span_text = tree.xpath('.//span[text()="Annual Total Return (%) History"]')

        #The table we wnat is in a div tag, which is a sibling to h3. The h3 and the div tag are under one overarching div tag. Get h3's sibiling
        h3 = h3_span_text[0].getparent()
        table = h3.getnext()

        #Grab all columns as lxml Element objects. This includes the 2 columns we don't want (placeholder value column + current year), so we need to filter them out.
        columns = [column for column in list(table)]

        #Assuming elements are in document order, we can just remove the first 2 elements of the list
        del columns[0:2]

        #Return filtered version
        return columns

    def build_json_response(self, column_data, fund_symbol):
        """
        Take the extracted column data and put it into a JSON response format for all data except current year.
        Converts list of column data as Element objects --> 2 dicts in the following format:
        {
            fund_symbol: {
                "2017": 27.95,
                ...
                "1996": 26.75
            },
            category: {
                "2017": 24.31,
                ...
                "1996": 13.5
            }
        }
        """

        current_year = str(datetime.datetime.now().year)
        fund = {}
        category = {}
        response = {}

        for col in column_data:
            data = [str(span.text_content()) for span in list(col)]
            if current_year not in data and len(data) == 4:    #Grab column data for all years except current year
                #Data will be in the format of a list of 4 elements, in the order [year, ui bar, fund return, category return]. We hardcode order, as Elements are returned in document order, according to documentation
                year = int(data[0])
                fund_return = float(data[2][:-1])           #Concatenate "%" off of string, then convert to float. Ex: "25.67%", we want: 25.67
                category_return = float(data[3][:-1])       #Concatenate "%" off of string, then convert to float. Ex: "25.67%", we want: 25.67
                fund[year] = fund_return
                category[year] = category_return

        response[fund_symbol] = fund
        response["Category"] = category
        return response



p = PerformanceStats()
fund_symbol = "PRHSX"
# print(p.get_10000_growth(fund_symbol))
# print(p.get_trailing_returns(fund_symbol))
# print(p.get_fund_historical_returns(fund_symbol))
print(p.get_performance_stats(fund_symbol))
