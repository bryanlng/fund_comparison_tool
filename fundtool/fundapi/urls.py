from django.conf.urls import url

from fundapi.views import PerformanceView

urlpatterns = [
    url(r'^v1/performance/(?P<fund_symbol>.*[^\?])$', PerformanceView.as_view()),
]
