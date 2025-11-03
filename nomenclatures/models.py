from django.db import models
from common.models import AuditableMixin
from common.utils.size_validators import SIZE_CHOICES



class Area(AuditableMixin):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=False, blank=False)
    
    class Meta:
        db_table = 'areas'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        
    def __str__(self):
        return self.name

class Species(AuditableMixin):
    name = models.CharField(max_length=100) 
    description = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'species'
        verbose_name = 'Especie'
        verbose_name_plural = 'Especies'
        
    def __str__(self):
        return self.name
    
class Breed(AuditableMixin):
    name = models.CharField(max_length=100) 
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, related_name='breeds', null=True, blank=True)
    size_category = models.CharField(max_length=100, choices=SIZE_CHOICES)
    
    class Meta:
        db_table = 'breeds'
        verbose_name = 'Raza'
        verbose_name_plural = 'Razas'
        
    def __str__(self):
        return self.name
    