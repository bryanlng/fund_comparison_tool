from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
# Create your tests here.

class PerformanceEndpointTest(TestCase):
    """
    This class defines the test suite for the PerformanceEndpointTest view.
    """

    DOMAINS_ENDPOINT = '/v1/performance/'

    def setUp(self):
        self.client = APIClient()
        self.headers = get_auth_header()

    def test_trailing_returns_good_symbol_name(self):
        data

    def test_trailing_returns_symbol_improper_syntax(self):
        dfdf

    def test_trailing_returns_symbol_not_exist(self):
        dfdf    
