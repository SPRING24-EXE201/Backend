from colorama import Fore
from django.http import JsonResponse


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            if response.status_code == 500:
                print(Fore.RED + f'Error: {response.content}')
                response = JsonResponse({
                    'message': 'Something went wrong!'
                }, status=500)
        except Exception as e:
            response = JsonResponse({
                    'message': 'Something went wrong!'
                }, status=500)
        return response
