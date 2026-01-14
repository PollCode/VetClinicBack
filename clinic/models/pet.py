import random
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from common.models import AuditableMixin


SEXO_CHOICES = [
    ('macho', 'macho'),
    ('hembra', 'hembra'),
]

ESTADO_REPRODUCTIVO_CHOICES = [
    ('vacio', 'vacio'),
    ('gestante', 'gestante'),
    ('lactacion', 'lactación'),
]

class Pet(AuditableMixin):
    code = models.CharField(max_length=8, unique=True, editable=False, verbose_name='Código')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    birth_date = models.DateField(verbose_name='Fecha de nacimiento')
    breed = models.ForeignKey('nomenclatures.Breed',on_delete=models.CASCADE, related_name='pets', verbose_name='Raza')
    client = models.ForeignKey('clinic.Client',on_delete=models.CASCADE, related_name='pets', verbose_name='Cliente')
    sex = models.CharField(max_length=100, choices=SEXO_CHOICES, verbose_name='Sexo')
    weight = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Peso')
    color = models.CharField(max_length=100, verbose_name='Color')
    reprod_state = models.CharField(max_length=100,choices=ESTADO_REPRODUCTIVO_CHOICES, verbose_name='Estado reproductivo', default='vacio')
    deleted = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='animales/', blank=True, null=True, verbose_name='Imagen')
    
    class Meta:
        db_table = 'pets'
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.generate_code()
        super().save(*args, **kwargs)
        
    def clean(self):
        super().clean()
        if self.weight is not None and self.breed:
            self.weight_validation()
        if self.birth_date is not None:
            self.birth_date_not_in_future()

    def generate_code(self):
        breed_prefix = slugify(self.breed.name)[:3].upper()
        random_number = str(random.randint(1000, 9999)).zfill(4)
        new_code = f"{breed_prefix}-{random_number}"
    
        while Pet.objects.filter(code=new_code).exists():
            random_number = str(random.randint(1000, 9999)).zfill(4)
            new_code = f"{breed_prefix}-{random_number}"
        
        self.code = new_code
        
    def weight_validation(self):
        value = self.weight
        size = self.breed.size_category
        
        if not value >= 1:
            raise ValidationError({'weight': 'El peso debe ser un número positivo'})
        
        match size:
            case 'toy':
                if value > 5:
                    raise ValidationError({'weight': 'El peso para un perro toy o enano debe ser entre 1 y 5 kilogramos'})
            case  'pequeño':
                if not 5 <= value <= 14:
                    raise ValidationError({'weight': 'El peso para un perro pequeño debe ser entre 5 y 14 kilogramos'})
            case  'mediano':
                if not 14 <= value <= 25:
                    raise ValidationError({'weight': 'El peso para un perro mediano debe ser entre 14 y 25 kilogramos'})
            case  'grande':
                if not 25 <= value <= 50:
                    raise ValidationError({'weight': 'El peso para un perro grande debe ser entre 25 y 50 kilogramos'})
            case  'gigante':
                if value < 50:
                    raise ValidationError({'weight': 'El peso para un perro gigante debe ser de 50 kilogramos o más'})            
            
            case  'gato_estandar':
                if value > 5:
                    raise ValidationError({'weight': 'El peso para un gato debe ser entre 1 y 5 kilogramos'})

    def birth_date_not_in_future(self):
        if self.birth_date > timezone.now().date():
         raise ValidationError({'birth_date': 'La fecha de nacimiento no puede ser posterior a la fecha actual.'})
    
    @property
    def species(self):
        return self.breed.species
    
    @property
    def age_in_months(self):
        today = timezone.now().date()
        delta = relativedelta(today, self.birth_date)
        return delta.years * 12 + delta.months
    
    @property
    def life_stage(self):
        size = self.breed.size_category
        age = self.age_in_months
        
        match size:
            case 'toy':
                if age <= 9:
                    return 'cachorro'
                elif 9 < age <= 84:
                    return 'adulto'
                else:
                    return 'senior'

            case 'pequeño':
                if age <= 12:
                    return 'cachorro'
                elif 12 < age <= 84:
                    return 'adulto'
                else:
                    return 'senior'

            case 'mediano':
                if age <= 15:
                    return 'cachorro'
                elif 15 < age <= 84:
                    return 'adulto'
                else:
                    return 'senior'

            case 'grande':
                if age <= 18:
                    return 'cachorro'
                elif 18 < age <= 84:
                    return 'adulto'
                else:
                    return 'senior'

            case 'gigante':
                if age <= 24:
                    return 'cachorro'
                elif 24 < age <= 84:
                    return 'adulto'
                else:
                    return 'senior'

            case 'gato_estandar':
                if age <= 6:
                    return 'cachorro'
                elif 6 < age <= 24:
                    return 'joven'
                elif 24 < age <= 72:
                    return 'adulto'
                elif 72 < age <= 120:
                    return 'adulto'
                else:
                    return 'senior'
        
    
        

class ClinicPage(AuditableMixin):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='clinic_pages', verbose_name='Mascota')
    # Examen médico general
    skin_mucosas = models.TextField(blank=True, null=True, verbose_name='Piel y Mucosas')
    respiratory_system = models.TextField(blank=True, null=True, verbose_name='Sistema Respiratorio')
    digestive_system = models.TextField(blank=True, null=True, verbose_name='Sistema Digestivo')
    circulatory_system = models.TextField(blank=True, null=True, verbose_name='Sistema Circulatorio')
    nervous_system = models.TextField(blank=True, null=True, verbose_name='Sistema Nervioso')
    locomotor_system = models.TextField(blank=True, null=True, verbose_name='Sistema Locomotor')
    reproductive_system = models.TextField(blank=True, null=True, verbose_name='Sistema Reproductor')
    pres_clinic_diag = models.TextField(blank=True, null=True, verbose_name='Diagnóstico Clínico Presuntivo')
    treatment = models.TextField(blank=True, null=True, verbose_name='Tratamiento')
    created_date = models.DateTimeField(verbose_name='created date', auto_now_add=True, unique_for_date=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'clinic_pages'
        verbose_name = 'Hoja Clínica'
        verbose_name_plural = 'Hojas Clínicas'

    def __str__(self):
        return f'Hist: {self.pet.name} - {self.created_date.strftime("%d/%m/%Y")}'