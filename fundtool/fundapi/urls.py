from django.conf.urls import url

from fundapi.views import PerformanceView
from fundapi.views import RiskView

urlpatterns = [
    url(r'^v1/performance/(?P<fund_symbol>.*[^\?])$', PerformanceView.as_view()),
    url(r'^v1/risk/(?P<fund_symbol>.*[^\?])$', RiskView.as_view()),
]
