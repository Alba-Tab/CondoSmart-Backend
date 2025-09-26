from django.db import models
from django.conf import settings
from core.mixins import AuditSaveMixin

class TimeStampedBy(AuditSaveMixin):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, 
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, 
        related_name="%(class)s_updated"
    )
    class Meta:
        abstract = True