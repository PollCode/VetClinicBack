from django.db import models
from common.models import AuditableMixin



class Area(AuditableMixin):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=False, blank=False)
    
    class Meta:
        db_table = 'areas'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        
    def __str__(self):
        return self.name
