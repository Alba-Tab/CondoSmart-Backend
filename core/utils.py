from typing import Optional
from django.http import HttpRequest

def get_client_ip(request: HttpRequest) -> Optional[str]:
    
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    return xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR")
