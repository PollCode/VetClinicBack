from django.db import models
from common.models import AuditableMixin
from django.core.validators import RegexValidator


class Client(AuditableMixin):
    # Validador para 11 dígitos exactos
    carnet_validator = RegexValidator(
        regex=r'^\d{11}$',
        message="El carnet debe tener exactamente 11 dígitos."
    )
    # Validador para 8 dígitos exactos
    phone_validator = RegexValidator(
        regex=r'^\d{8}$',
        message="El teléfono debe tener exactamente 8 dígitos."
    )
    
    name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    carnet = models.CharField(max_length=11, validators=[carnet_validator], verbose_name='Carnet')
    address = models.CharField(max_length=200, verbose_name='Dirección', blank=True, null=True)
    phone_number = models.CharField(max_length=8, validators=[phone_validator], verbose_name='Número de teléfono', blank=True, null=True)
    deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'clients'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        
    def __str__(self):
        return f'{self.name} {self.last_name}'