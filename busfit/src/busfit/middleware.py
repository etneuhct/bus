class AjaxRedirectMiddleware(object):
    """
    Set special status code on HTTP response when redirecting

    Ajax clients won't recognize redirects on their own. So this
    will help checking and identifying redirecting responses in a Javascript AJAX request handler.
    """
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.is_ajax():
            if response.status_code == 302 or response.status_code == 301:
                response.status_code = 278
        return response

    # for compatibility with pre-Django1.10 versions
    def process_response(self, request, response):
        if request.is_ajax():
            if response.status_code == 302 or response.status_code == 301:
                response.status_code = 278
        return response


class AjaxRequestExceptionMiddleware(object):
    """
    Return appropriate JsonResponse on code exception instead of html error page.

    Ajax clients should only expect json. As such, this will send a json "errors object"
    whenever an exception occurs on our end.
    """
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)

    def process_exception(self, request, exception):
        from django.conf import settings
        from django.http import JsonResponse
        if settings.DEBUG:
            return JsonResponse({'success': False, 'error': exception.message,}, status=500)
        return JsonResponse({'success': False }, status=500)
