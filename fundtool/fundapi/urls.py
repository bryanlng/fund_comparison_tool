from django.conf.urls import url

from fundapi.views import PerformanceView, RiskView, GeneralView, HoldingsView

urlpatterns = [
    url(r'^v1/performance/(?P<fund_symbol>.*[^\?])$', PerformanceView.as_view()),
    url(r'^v1/risk/(?P<fund_symbol>.*[^\?])$', RiskView.as_view()),
    url(r'^v1/general/(?P<fund_symbol>.*[^\?])$', GeneralView.as_view()),
    url(r'^v1/holdings/(?P<fund_symbol>.*[^\?])$', HoldingsView.as_view()),
]
