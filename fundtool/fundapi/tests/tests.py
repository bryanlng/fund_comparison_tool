from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
# Create your tests here.

class PerformanceEndpointTest(TestCase):
    """This class defines the test suite for the bucketlist model."""

    def setUp(self):
        self.client = APIClient()
