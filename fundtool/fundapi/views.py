from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

import fundtool.fundapi.libraries.exceptions as FundException

import fundtool.fundapi.libraries.PerformanceStats


# Create your views here.
class PerformanceView(APIView):
    def get(self, request, fund_symbol):
        """
        An endpoint to grab Performance data for a fund
        """

        response = {}
        request_status = status.HTTP_200_OK
        try:
            p = PerformanceStats()
            response = p.get_performance_stats(fund_symbol)

        except FundException.SymbolDoesNotExistError as e:
            request_status = e.request_status
        except FundException.UIChangedError as e:
            request_status = e.request_status
        except FundException.SourceEndpointChangedError as e:
            request_status = e.request_status

        return JsonResponse(response, json_dumps_params=extra_params, status=request_status)
