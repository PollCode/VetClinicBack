from django.db import models
from common.models import AuditableMixin
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from nomenclatures.models import Area


class User(AuditableMixin, AbstractUser):
    
    class Role(models.TextChoices):
        ADMINISTRADOR = 'admin'
        DOCTOR = 'doctor'
        SECTRETARIA = 'secretaria'
        LABORATORISTA = 'laboratorista'
        DEFAULT = 'default'

    username = models.CharField(max_length=100, unique=True)
    rol = models.CharField(max_length=100, choices=Role.choices, default=Role.DEFAULT)
    area = models.ForeignKey(Area, related_name="users", on_delete=models.SET_NULL, null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password',]
    
    class Meta:
        db_table = 'users'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        
    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'access': str(refresh.access_token), 'refresh': str(refresh),}
    