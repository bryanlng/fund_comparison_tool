from rest_framework import status

class SymbolDoesNotExistError(Exception):
    request_status = status.HTTP_400_BAD_REQUEST


class UIChangedError(Exception):
    request_status = status.HTTP_500_INTERNAL_SERVER_ERROR


class SourceEndpointChangedError(Exception):
    request_status = status.HTTP_500_INTERNAL_SERVER_ERROR
