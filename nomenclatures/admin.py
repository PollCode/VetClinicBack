from django.contrib import admin
from .models import Area

class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', )
    readonly_fields = (
        'created_date',
        'created_by',
        'updated_date',
        'updated_by',
        'deleted_date',
        'deleted_by'
    )
    
admin.site.register(Area, AreaAdmin)