from django.contrib import admin
from .models.client import Client
from .models.pet import Pet, ClinicPage


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'last_name',
        'carnet',
        'address',
        'phone_number',
    )
    readonly_fields = (
        'created_date',
        'created_by',
        'updated_date',
        'updated_by',
        'deleted_date',
        'deleted_by'
    )

class PetAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'code',
        'name',
        'birth_date',
        'breed',
        'client',
        'sex',
        'weight',
        'color',
        'reprod_state',
    )
    readonly_fields = (
        'created_date',
        'created_by',
        'updated_date',
        'updated_by',
        'deleted_date',
        'deleted_by'
    )


class ClinicPageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pet',
        'skin_mucosas',
        'respiratory_system',
        'digestive_system',
        'circulatory_system',
        'nervous_system',
        'locomotor_system',
        'reproductive_system',
        'pres_clinic_diag',
        'treatment',
    )
    readonly_fields = (
        'created_date',
        'created_by',
        'updated_date',
        'updated_by',
        'deleted_date',
        'deleted_by'
    )

   
admin.site.register(Client, ClientAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(ClinicPage, ClinicPageAdmin)