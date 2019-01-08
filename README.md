# Mutual Fund Comparison Tool (currently under construction!)
![](https://img.shields.io/badge/Python-3.6-blue.svg)
![](https://img.shields.io/badge/Django-2.1.2-yellow.svg)
![](https://img.shields.io/badge/django_rest_framework-3.8.2-orange.svg)
![](https://img.shields.io/badge/Build_Status-Coming_Soon-green.svg)
![](https://img.shields.io/badge/Coverage-Coming_Soon-green.svg)


## Update
REST API is finally deployed! [link](http://www.comparemutualfunds.co.uk/v1/performance/PRHSX)


## About
This tool allows a user to compare multiple mutual funds, side by side, on a variety of vectors (Performance, Risk, etc),
so they can make the best, unbiased decision on an investment.

## Usage
Currently, only the backend has been developed.
To get the stats of a mutual fund, type in the following URL:
"www.comparemutualfunds.co.uk/v1/performance/<5 letter fund symbol>"


For example:
Vanguard 500 Index Fund Admiral Shares (VFIAX)

[http://www.comparemutualfunds.co.uk/v1/performance/VFIAX](http://www.comparemutualfunds.co.uk/v1/performance/VFIAX)


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

## Deploying:
I used AWS Elastic Beanstalk to deploy this Django project, and Route 53 to register the domain name. Tutorials can be found at this [link](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html) and this [link](https://aws.amazon.com/getting-started/tutorials/get-a-domain/) as well as at the bottom of the page, but in case the links are broken, here are the following steps to deploying:

### [Deploying onto AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)
1. Go to the fundtool directory
```
cd fundtool
```

2. Create a directory called ".ebextensions", and cd into it
```
mkdir .ebextensions
cd .ebextensions
```

3. Create a file called "django.config", and place the following text inside:
```
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: fundtool/wsgi.py
```

4. Initialize your EB CLI repository with the eb init command: 
```
eb init -p python-3.6 django-tutorial

...where django-tutorial is the name of the AWS EB application
```

5. Create an environment and deploy you application to it with eb create:
```
eb create django-env

...where django-env is the name of the AWS EB environment
```

6. When the environment creation process completes, find the domain name of your new environment by running eb status:
```
eb status
Environment details for: django-env
  Application name: django-tutorial
  ...
  CNAME: eb-django-app-dev.elasticbeanstalk.com
  ...
```

7. Edit the settings.py file in the ebdjango directory, locate the ALLOWED_HOSTS setting, and then add your application's domain name that you found in the previous step to the setting's value. If you can't find this setting in the file, add it to a new line. 
```
...
ALLOWED_HOSTS = ['eb-django-app-dev.elasticbeanstalk.com']
```

8. Save the file, and then deploy your application by running eb deploy. When you run eb deploy, the EB CLI bundles up the contents of your project directory and deploys it to your environment. 
```
eb deploy   
```

9. Open the website by typing eb open. If an error shows up, append the http path "/v1/performance/<fund_name>" to the url
```
eb open
```

### [Registering the domain name](https://aws.amazon.com/getting-started/tutorials/get-a-domain/)
#### Step 1: Registering the domain name
1. Open the Route 53 console on your AWS account, located [here](https://console.aws.amazon.com/route53/home?region=us-east-1)
2. Under Domain Registration, click "Get Started Now"
3. Click "Register Domain", and choose a name and TLD. Enter contact details and then complete the purchase

#### Step 2: Configuring DNS
1. Go back to the Route 53 console on your AWS account, located [here](https://console.aws.amazon.com/route53/home?region=us-east-1)
2. Under Hosted Zones, click on the domain you chose.
3. Click on the button "Create Record Set". Here, we'll be creating a Fully Qualified Domain Name. 
   1. Under "Name", type "www"
   2. Under "Type", put "A - IPv4 address"
   3. Under "Alias Target", choose the option under "Elastic Load Balancers". The correct target should be the corresponding CNAME of your  AWS EB environment. You can double check this by typing in "eb status" into a terminal.
   4. Under "Routing Policy", choose "Simple".
   5. Under "Evaluate Target Health", choose "no".
  


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
