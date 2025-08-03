from django.http import JsonResponse


def hello(request):
    """Return a simple JSON response for the React frontend."""
    return JsonResponse({"message": "Hello from Django"})
