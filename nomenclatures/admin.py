from django.contrib import admin
from .models import Area, Breed

class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', )
    search_fields = ('name',)
    list_filter = ('name',)
    readonly_fields = (
        'created_date',
        'created_by',
        'updated_date',
        'updated_by',
        'deleted_date',
        'deleted_by'
    )
    
    
class BreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'species', 'size_category')
    search_fields = ('name', 'species')
    list_filter = ('name', 'species')
    readonly_fields = (
        'created_date',
        'created_by',
        'updated_date',
        'updated_by',
        'deleted_date',
        'deleted_by',
    )
    
admin.site.register(Area, AreaAdmin)
admin.site.register(Breed, BreedAdmin)