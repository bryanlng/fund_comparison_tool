from rest_framework import status

class ImproperSymbolFormatError(Exception):
    request_status = status.HTTP_400_BAD_REQUEST

class SymbolDoesNotExistError(Exception):
    request_status = status.HTTP_404_NOT_FOUND

class UIChangedError(Exception):
    request_status = status.HTTP_500_INTERNAL_SERVER_ERROR

class SourceEndpointChangedError(Exception):
    request_status = status.HTTP_500_INTERNAL_SERVER_ERROR
