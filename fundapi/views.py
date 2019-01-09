from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.throttling import UserRateThrottle

from fundapi.libraries.Performance import PerformanceStats
from fundapi.libraries.Risk import RiskStats
from fundapi.libraries.General import GeneralStats
from fundapi.libraries.Holdings import HoldingsStats
import fundapi.libraries.exceptions as FundException


# Create your views here.
class PerformanceView(APIView):
    throttle_classes = (UserRateThrottle,)

    def get(self, request, fund_symbol):
        """
        An endpoint to grab Performance data for a fund
        ---
            - code: 200
              message: Symbol name valid, all data
            - code: 400
              message: improper syntax on symbol name (ex: 1ef3d)
            - code: 404
              message: symbol name doesn't exist, but has the correct format (ex: AAAAA)
            - code: 500
              message: Source endpoints we scrape from 1) UI changed, 2) Endpoint is down/changed
        """

        response = {}

        extra_params = {}
        if "pretty" in request.GET:
            extra_params = {
                "indent": 4,
                "sort_keys": True
            }

        request_status = status.HTTP_200_OK
        try:
            print("host header: {}".format(request.META['HTTP_HOST']))
            p = PerformanceStats()
            response = p.get_performance_stats(fund_symbol)

        except FundException.ImproperSymbolFormatError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.SymbolDoesNotExistError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.UIChangedError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.SourceEndpointChangedError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status

        return JsonResponse(response, json_dumps_params=extra_params, status=request_status)


class RiskView(APIView):
    throttle_classes = (UserRateThrottle,)
    def get(self, request, fund_symbol):
        """
        An endpoint to grab Performance data for a fund
        ---
            - code: 200
              message: Symbol name valid, all data
            - code: 400
              message: improper syntax on symbol name (ex: 1ef3d)
            - code: 404
              message: symbol name doesn't exist, but has the correct format (ex: AAAAA)
            - code: 500
              message: Source endpoints we scrape from 1) UI changed, 2) Endpoint is down/changed
        """

        response = {}

        extra_params = {}
        if "pretty" in request.GET:
            extra_params = {
                "indent": 4,
                "sort_keys": True
            }

        request_status = status.HTTP_200_OK
        try:
            r = RiskStats()
            response = r.get_risk_stats(fund_symbol)

        except FundException.ImproperSymbolFormatError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.SymbolDoesNotExistError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.UIChangedError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.SourceEndpointChangedError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status

        return JsonResponse(response, json_dumps_params=extra_params, status=request_status)


class GeneralView(APIView):
    throttle_classes = (UserRateThrottle,)
    def get(self, request, fund_symbol):
        """
        An endpoint to grab Performance data for a fund
        ---
            - code: 200
              message: Symbol name valid, all data
            - code: 400
              message: improper syntax on symbol name (ex: 1ef3d)
            - code: 404
              message: symbol name doesn't exist, but has the correct format (ex: AAAAA)
            - code: 500
              message: Source endpoints we scrape from 1) UI changed, 2) Endpoint is down/changed
        """

        response = {}

        extra_params = {}
        if "pretty" in request.GET:
            extra_params = {
                "indent": 4,
                "sort_keys": True
            }

        request_status = status.HTTP_200_OK
        try:
            g = GeneralStats()
            response = g.get_general_stats(fund_symbol)

        except FundException.ImproperSymbolFormatError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.SymbolDoesNotExistError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.UIChangedError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.SourceEndpointChangedError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status

        return JsonResponse(response, json_dumps_params=extra_params, status=request_status)


class HoldingsView(APIView):
    throttle_classes = (UserRateThrottle,)
    def get(self, request, fund_symbol):
        """
        An endpoint to grab Performance data for a fund
        ---
            - code: 200
              message: Symbol name valid, all data
            - code: 400
              message: improper syntax on symbol name (ex: 1ef3d)
            - code: 404
              message: symbol name doesn't exist, but has the correct format (ex: AAAAA)
            - code: 500
              message: Source endpoints we scrape from 1) UI changed, 2) Endpoint is down/changed
        """

        response = {}

        extra_params = {}
        if "pretty" in request.GET:
            extra_params = {
                "indent": 4,
                "sort_keys": True
            }

        request_status = status.HTTP_200_OK
        try:
            h = HoldingsStats()
            response = h.get_holdings_stats(fund_symbol)

        except FundException.ImproperSymbolFormatError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.SymbolDoesNotExistError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.UIChangedError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status
        except FundException.SourceEndpointChangedError as e:
            request_status = e.request_status
            response["error"] = str(e.args[0])
            response["HTTP_ERROR_CODE"] = request_status

        return JsonResponse(response, json_dumps_params=extra_params, status=request_status)
