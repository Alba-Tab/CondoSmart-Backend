from django.db import models
from django.conf import settings


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class TimeStampedBy(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    ## Managers
    objects = ActiveManager()      # solo activos
    all_objects = models.Manager()     # incluye eliminados
    
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
        
    def set_active(self, active: bool, user=None):
        if active != self.is_active:
            self.is_active = active
            if user:
                self.updated_by = user
            self.save(update_fields=["is_active", "updated_by", "updated_at"])