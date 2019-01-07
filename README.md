# Mutual Fund Comparison Tool (currently under construction!)
![](https://img.shields.io/badge/Python-3.6-blue.svg)
![](https://img.shields.io/badge/Django-2.1.2-yellow.svg)
![](https://img.shields.io/badge/django_rest_framework-3.8.2-orange.svg)
![](https://img.shields.io/badge/Build_Status-Coming_Soon-green.svg)
![](https://img.shields.io/badge/Coverage-Coming_Soon-green.svg)


## Update
REST API is finally deployed! [link](http://www.comparemutualfunds.co.uk/v1/performance/PRHSX)


I'm working on getting a link to a domain hosted on Route 53 up and running.

## About
This tool allows a user to compare multiple mutual funds, side by side, on a variety of vectors (Performance, Risk, etc),
so they can make the best, unbiased decision on an investment.

### Purpose
To create a better tool for comparing mutual funds. The majority of the currently available tools are either incredibly difficult to use, or are unable to provide enough information to make a solid decision. Currently, the best option out there is [Markets.ft](https://markets.ft.com/data/funds/us/compare), but even they don't provide enough information to make a solid investment decision.

As an investor, I want to know as much information as possible about the mutual funds that I might potentially put thousands of dollars into. In addition, I want to be able to compare mutual funds in a seamless and efficient fashion; getting the information I need shouldn't be a nuisance.

## Documentation:
Documentation for the internal REST API is on [Apiary](https://mutualfundcomparisontoolapi.docs.apiary.io/#)

## Backlog of items to complete:
https://trello.com/b/p1mWpgjU

## Installation:
```
pip install -r requirements.txt
cd fundtool
python3 manage.py runserver
Open up a browser and go to http://127.0.0.1:8000/v1/performance/PRHSX
```

## Local testing:
```
cd fundtool
python3 manage.py runserver
Open up a browser and go to http://127.0.0.1:8000/v1/performance/PRHSX
```

## Deploying (coming soon once I figure this part out):

## Sources I pull from:
### Basic summary:
I used BeautifulSoup 4 and lxml to scrape data from the following sites:
1. Yahoo Finance
2. MorningStar
3. Markets.ft

### Actual urls:
For this example, I used PRHSX. Replace with actual mutual fund symbol (5 letter, all caps, no spaces)

#### I. Performance:
   1. [Morningstar Trailing Returns](http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=PRHSX&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype=)
   2. [Markets.ft Hypothetical growth of $10000](https://markets.ft.com/data/funds/ajax/US/get-comparison-panel?data={"comparisons":["PRHSX"],"openPanels":["Performance"]})
   3. [Yahoo Finance Historical Returns](https://finance.yahoo.com/quote/PRHSX/performance?p=PRHSX)

#### II. Risk:
   1. [Morningstar Risk MPT Stats](http://performance.morningstar.com/ratrisk/RatingRisk/fund/mpt-statistics.action?&t=PRHSX&region=usa&culture=en-US&cur=&ops=clear&s=0P00001L8R&y=3&ep=true&comparisonRemove=true&benchmarkSecId=&benchmarktype=)
   2. [Morningstar Volatility Measurements](http://performance.morningstar.com/ratrisk/RatingRisk/fund/volatility-measurements.action?&t=PRHSX&region=usa&culture=en-US&cur=&ops=clear&s=0P00001L8R&y=3&ep=true&comparisonRemove=true&benchmarkSecId=&benchmarktype=)
   3. [Morningstar Capture Ratios](http://performance.morningstar.com/ratrisk/RatingRisk/fund/updownside-capture.action?&t=PRHSX&region=usa&culture=en-US&cur=&ops=clear&s=0P00001L8R&ep=true&comparisonRemove=null&benchmarkSecId=&benchmarktype=)
   
#### III. General Stats:
   1. [Morningstar General Stats](https://quotes.morningstar.com/fundq/c-header?&t=PRHSX&region=usa&culture=en-US&version=RET&cur=&test=QuoteiFrame)
   2. [Morningstar Asset Allocation](https://quotes.morningstar.com/fundq/c-assetAllocation?&t=PRHSX&region=usa&culture=en-US&version=RET&cur=&test=QuoteiFrame)
   3. [Morningstar Risk & Return vs Category](https://quotes.morningstar.com/fundq/c-risk-measures?&t=PRHSX&region=usa&culture=en-US&version=RET&cur=&test=QuoteiFrame)
   4. [Morningstar Overall Rating](https://www.morningstar.com/api/v1/security-identifier/0P00002WFU)
   5. [Morningstar Quotes](https://www.morningstar.com/funds/XNAS/PRHSX/quote.html)
   
#### IV. Top 25 Holdings:
   1. [Morningstar Top 25 Holdings](http://portfolios.morningstar.com/portfo/fund/ajax/holdings_tab?t=PRHSX&region=usa&culture=en-US&cur=&dataType=0&sortby=weighting&order=des)


## Example that I used to build the backend and deploy it:
   1. https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-1
   2. https://blog.sicara.com/deploy-serverless-rest-api-lambda-s3-aws-2cf99b8f34ae
   3. https://www.django-rest-framework.org/api-guide/throttling/
   4. https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html
   5. https://aws.amazon.com/getting-started/tutorials/get-a-domain/
