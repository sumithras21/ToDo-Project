import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()
        duration = end_time - start_time

        print(f"[MIDDLEWARE] {request.method} {request.path} took {duration:.4f} sec")

        return response