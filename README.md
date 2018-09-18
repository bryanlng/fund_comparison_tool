# Mutual Fund Comparison Tool

## Documentation:
Documentation for the internal REST API is on [Apiary](https://mutualfundcomparisontoolapi.docs.apiary.io/#)

## Trello board:
https://trello.com/b/p1mWpgjU

## Installation:
```

pip install -r requirements.txt
cd fundtool
python3 manage.py runserver
Open up a browser and go to http://127.0.0.1:8000/v1/performance/PRHSX
   PRHSX is just an example; feel free to use any other valid fund symbol name
```
Example:    [http://127.0.0.1:8000/v1/performance/PRHSX](http://127.0.0.1:8000/v1/performance/PRHSX)

## Sources I pull from:
### Basic summary:
1. Yahoo Finance
2. MorningStar
3. Markets.ft

### Actual urls:
For this example, I used PRHSX. Replace with actual mutual fund symbol (5 letter, all caps, no spaces)

I. Performance:
   1. [Trailing Returns](http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=PRHSX>&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype=)
   2. [Hypothetical growth of $10000](https://markets.ft.com/data/funds/ajax/US/get-comparison-panel?data={"comparisons":["PRHSX"],"openPanels":["Performance"]})
   3. [Historical returns](https://finance.yahoo.com/quote/PRHSX/performance?p=PRHSX)



## Example that I used to build the backend:
https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-1






## Markdown help cause I'm a noob
https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
https://en.support.wordpress.com/markdown-quick-reference/
