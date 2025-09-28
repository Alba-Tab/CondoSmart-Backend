from django.db import models
from django.conf import settings

from django.utils import timezone

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # por defecto solo devuelve no eliminados
        return super().get_queryset().filter(is_deleted=False)

class TimeStampedBy(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_deleted = models.BooleanField(default=False)
    
    #is_deleted = models.BooleanField(default=False)
    #deleted_at = models.DateTimeField(null=True, blank=True)
    #deleted_by = models.ForeignKey(
    #    settings.AUTH_USER_MODEL, null=True, blank=True,
    #    on_delete=models.SET_NULL, related_name="%(class)s_deleted"
    #)
#
    ## Managers
    #objects = SoftDeleteManager()      # solo activos
    #all_objects = models.Manager()     # incluye eliminados
    
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
        
    #def delete(self, using=None, keep_parents=False, user=None):
    #    """Soft delete: marca como borrado en vez de eliminar físicamente"""
    #    self.is_deleted = True
    #    self.deleted_at = timezone.now()
    #    if user:
    #        self.deleted_by = user
    #    self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])