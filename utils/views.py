from django.http import JsonResponse


def error_404(request, exception):
    message = ('The endpoint is not found.')
    response = JsonResponse(data={'error': message, 'status_code': 404})
    response.status_code = 404
    return response


def error_500(request):
    message = ('An error occurred on server.')
    response = JsonResponse(data={'error': message, 'status_code': 500})
    response.status_code = 500
    return response