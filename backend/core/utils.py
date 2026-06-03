from rest_framework.response import Response

def api_response(success=True, data=None, error=None, status=200):
    """
    Standard API response wrapper for JSM Shiksha Academy.
    """
    return Response({
        "success": success,
        "data": data,
        "error": error
    }, status=status)
