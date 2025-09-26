import threading

_thread_locals = threading.local()

def get_user():
    return getattr(_thread_locals, "user", None)

class UserMiddleware:
    """Guarda el usuario actual en thread local para usar en modelos."""
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        _thread_locals.user = getattr(request, "user", None)
        return self.get_response(request)
