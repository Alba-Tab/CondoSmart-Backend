from typing import Optional
from django.http import HttpRequest
from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 200
    
def get_client_ip(request: HttpRequest) -> Optional[str]:
    
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    return xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR")
