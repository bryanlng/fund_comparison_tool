import fundapi.libraries.exceptions as FundException
from enum import Enum
import re

class Section(Enum):
    TRAILING = "trailing_returns"
    GROWTH = "10000_growth"
    HISTORICAL = "historical"
    RISK_MPT = "risk_modern_portfolio_theory_stats"
    RISK_VOLATILITY = "risk_volatility"
    CAPTURE_RATIOS = "capture_ratios"

def build_url(section, fund_symbol, year=0):
    if section == Section.TRAILING:
        return "http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=" + fund_symbol + "&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype="
    elif section == Section.GROWTH:
        return "https://markets.ft.com/data/funds/ajax/US/get-comparison-panel?data={\"comparisons\":[\"" + fund_symbol + "\"],\"openPanels\":[\"Performance\"]}"
    elif section == Section.HISTORICAL:
        return "https://finance.yahoo.com/quote/" + fund_symbol + "/performance?p=" + fund_symbol
    elif section == Section.RISK_MPT:
        return "http://performance.morningstar.com/ratrisk/RatingRisk/fund/mpt-statistics.action?&t=" + fund_symbol + "&region=usa&culture=en-US&cur=&ops=clear&s=0P00001L8R&y=" + year + "&ep=true&comparisonRemove=true&benchmarkSecId=&benchmarktype="
    elif section == Section.RISK_VOLATILITY:
        return "http://performance.morningstar.com/ratrisk/RatingRisk/fund/volatility-measurements.action?&t=" + fund_symbol + "&region=usa&culture=en-US&cur=&ops=clear&s=0P00001L8R&y=" + year + "&ep=true&comparisonRemove=true&benchmarkSecId=&benchmarktype="
    elif section == Section.CAPTURE_RATIOS:
        return "http://performance.morningstar.com/ratrisk/RatingRisk/fund/updownside-capture.action?&t=" + fund_symbol + "&region=usa&culture=en-US&cur=&ops=clear&s=0P00001L8R&ep=true&comparisonRemove=null&benchmarkSecId=&benchmarktype="
    else:
        return "wut"

def validate_format(fund_symbol):
    if len(fund_symbol) != 5 or re.match('^[A-Z]{5}$', fund_symbol) is None:
        raise FundException.ImproperSymbolFormatError(f"Fund symbol is not in the proper format (needs to be 5 characters, capitalized, no spaces, A-Z): {fund_symbol}")
