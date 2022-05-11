from rest_framework.views import exception_handler
from rest_framework.views import Response
from rest_framework import status


def responst_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if (response is None):
        return Response({
            'errorMessage': '服务器错误',
            'errorData': exc.args
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
    else:
        if isinstance(exc.detail, str):
            errorMessage = exc.detail
        else:
            errorMessage = exc.default_detail

        return Response({
            'errorMessage': errorMessage,
            'errorData': exc.detail
        }, status=response.status_code, exception=True)
