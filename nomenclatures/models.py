from django.db import models
from common.models import AuditableMixin


SPECIES_CHOICES = [
    ('canino', 'Canino'),
    ('felino', 'Felino'),
]
    

SIZE_CHOICES = [
    ('toy', 'Toy/Enano'),
    ('pequeño', 'Pequeño'),
    ('mediano', 'Mediano'),
    ('grande', 'Grande'),
    ('gigante', 'Gigante'),
    ('gato_estandar', 'Gato Estandar'),
]


class Area(AuditableMixin):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    description = models.CharField(max_length=100, null=False, blank=False)
    
    class Meta:
        db_table = 'areas'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        
    def __str__(self):
        return self.name
    
class Breed(AuditableMixin):

    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre") 
    species = models.CharField(max_length=100,verbose_name="Especie", choices=SPECIES_CHOICES)
    size_category = models.CharField(max_length=100, choices=SIZE_CHOICES)
    
    class Meta:
        db_table = 'breeds'
        verbose_name = 'Raza'
        verbose_name_plural = 'Razas'
        
    def __str__(self):
        return self.name
    